/**
 * Persistent Context Backend - Use Playwright's persistent browser profile
 *
 * This backend uses Playwright's launchPersistentContext to maintain
 * browser state (cookies, localStorage) across sessions in a dedicated
 * Chrome profile directory.
 */

import { chromium, type BrowserContext, type Page } from 'playwright';
import { mkdir, access, rm, readFile, writeFile } from 'fs/promises';
import { join } from 'path';
import { homedir } from 'os';
import type { AuthBackend, AuthResult, AuthConfig, Cookie } from '../types.js';

export class PersistentAuthBackend implements AuthBackend {
  name = 'persistent' as const;
  priority = 3;

  private profilePath: string;
  private stateFile: string;

  constructor(private config: AuthConfig) {
    // Expand ~ to home directory
    this.profilePath = config.profileDir.replace(/^~/, homedir());
    this.stateFile = join(this.profilePath, 'auth-state.json');
  }

  /**
   * Always available as a fallback
   */
  async isAvailable(): Promise<boolean> {
    return true;
  }

  /**
   * Authenticate using persistent browser context
   */
  async authenticate(): Promise<AuthResult> {
    // First check if we have stored state
    const stored = await this.getStoredAuth();
    if (stored?.success) {
      return stored;
    }

    // Need to do interactive login
    return {
      success: false,
      backend: this.name,
      message: 'No valid session in persistent profile. Manual login required.',
      profilePath: this.profilePath,
    };
  }

  /**
   * Get stored authentication from persistent profile
   */
  async getStoredAuth(): Promise<AuthResult | null> {
    try {
      // Check if state file exists
      await access(this.stateFile);

      const stateJson = await readFile(this.stateFile, 'utf-8');
      const state = JSON.parse(stateJson) as {
        cookies: Cookie[];
        savedAt: string;
      };

      // Validate cookies haven't expired
      const now = Date.now() / 1000;
      const validCookies = state.cookies.filter(c =>
        c.expires === -1 || c.expires > now
      );

      // Check for essential auth cookies
      const hasAuthCookies = validCookies.some(c =>
        ['SID', 'HSID', 'SSID', '__Secure-1PSID'].includes(c.name)
      );

      if (!hasAuthCookies) {
        return null;
      }

      return {
        success: true,
        backend: this.name,
        message: `Loaded session from persistent profile (saved: ${state.savedAt})`,
        cookies: validCookies,
        profilePath: this.profilePath,
      };
    } catch {
      return null;
    }
  }

  /**
   * Launch persistent context for manual login
   */
  async launchForLogin(): Promise<{
    context: BrowserContext;
    page: Page;
    saveAndClose: () => Promise<AuthResult>;
  }> {
    // Ensure profile directory exists
    await mkdir(this.profilePath, { recursive: true });

    const context = await chromium.launchPersistentContext(this.profilePath, {
      headless: false, // Must be visible for manual login
      channel: 'chrome', // Use installed Chrome
      viewport: { width: 1280, height: 720 },
      args: [
        '--disable-blink-features=AutomationControlled',
        '--no-first-run',
        '--no-default-browser-check',
      ],
    });

    const page = await context.newPage();
    await page.goto(this.config.notebookLmUrl);

    const saveAndClose = async (): Promise<AuthResult> => {
      try {
        // Get all cookies
        const allCookies = await context.cookies();
        const authCookies = allCookies.filter(c =>
          c.domain.includes('google.com') || c.domain.includes('notebooklm')
        );

        // Check if logged in
        const hasAuthCookies = authCookies.some(c =>
          ['SID', 'HSID', 'SSID', '__Secure-1PSID'].includes(c.name)
        );

        if (!hasAuthCookies) {
          await context.close();
          return {
            success: false,
            backend: this.name,
            message: 'Login not detected. Please complete the Google login.',
          };
        }

        // Save state to file
        const cookies = this.convertCookies(authCookies);
        await this.saveState(cookies);

        await context.close();

        return {
          success: true,
          backend: this.name,
          message: 'Successfully logged in and saved session to persistent profile',
          cookies,
          profilePath: this.profilePath,
        };
      } catch (error) {
        await context.close();
        throw error;
      }
    };

    return { context, page, saveAndClose };
  }

  /**
   * Create a new context with stored cookies (for headless use)
   */
  async createContextWithStoredAuth(): Promise<BrowserContext | null> {
    const stored = await this.getStoredAuth();
    if (!stored?.cookies) {
      return null;
    }

    // Launch new browser and inject cookies
    const browser = await chromium.launch({
      headless: true,
      channel: 'chrome',
    });

    const context = await browser.newContext();

    // Convert our cookies back to Playwright format
    const playwrightCookies = stored.cookies.map(c => ({
      name: c.name,
      value: c.value,
      domain: c.domain,
      path: c.path,
      expires: c.expires,
      httpOnly: c.httpOnly,
      secure: c.secure,
      sameSite: c.sameSite as 'Strict' | 'Lax' | 'None',
    }));

    await context.addCookies(playwrightCookies);

    return context;
  }

  /**
   * Clear stored authentication
   */
  async clearAuth(): Promise<void> {
    try {
      await rm(this.stateFile, { force: true });
      // Optionally clear the entire profile
      // await rm(this.profilePath, { recursive: true, force: true });
    } catch {
      // Ignore errors
    }
  }

  /**
   * Save authentication state to file
   */
  private async saveState(cookies: Cookie[]): Promise<void> {
    await mkdir(this.profilePath, { recursive: true });

    const state = {
      cookies,
      savedAt: new Date().toISOString(),
    };

    await writeFile(this.stateFile, JSON.stringify(state, null, 2));
  }

  /**
   * Convert Playwright cookies to our Cookie type
   */
  private convertCookies(playwrightCookies: Array<{
    name: string;
    value: string;
    domain: string;
    path: string;
    expires: number;
    httpOnly: boolean;
    secure: boolean;
    sameSite: 'Strict' | 'Lax' | 'None';
  }>): Cookie[] {
    return playwrightCookies.map(c => ({
      name: c.name,
      value: c.value,
      domain: c.domain,
      path: c.path,
      expires: c.expires,
      httpOnly: c.httpOnly,
      secure: c.secure,
      sameSite: c.sameSite,
    }));
  }
}

/**
 * Get profile status
 */
export async function getProfileStatus(config: AuthConfig): Promise<{
  exists: boolean;
  hasState: boolean;
  savedAt: string | null;
  profilePath: string;
}> {
  const profilePath = config.profileDir.replace(/^~/, homedir());
  const stateFile = join(profilePath, 'auth-state.json');

  try {
    await access(profilePath);
    const exists = true;

    try {
      const stateJson = await readFile(stateFile, 'utf-8');
      const state = JSON.parse(stateJson) as { savedAt?: string };
      return {
        exists,
        hasState: true,
        savedAt: state.savedAt || null,
        profilePath,
      };
    } catch {
      return { exists, hasState: false, savedAt: null, profilePath };
    }
  } catch {
    return { exists: false, hasState: false, savedAt: null, profilePath };
  }
}
