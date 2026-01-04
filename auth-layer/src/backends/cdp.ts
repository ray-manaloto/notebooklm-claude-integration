/**
 * CDP Backend - Connect to existing Chrome browser via Chrome DevTools Protocol
 *
 * This backend connects to a Chrome instance that's already running with
 * --remote-debugging-port enabled. If the user is already logged into
 * NotebookLM in that browser, we can reuse their session.
 */

import { chromium, type Page } from 'playwright';
import type { AuthBackend, AuthResult, AuthConfig, Cookie } from '../types.js';

export class CDPAuthBackend implements AuthBackend {
  name = 'cdp' as const;
  priority = 1; // Highest priority - best UX

  constructor(private config: AuthConfig) {}

  /**
   * Check if Chrome is running with remote debugging enabled
   */
  async isAvailable(): Promise<boolean> {
    try {
      const response = await fetch(`http://localhost:${this.config.cdpPort}/json/version`, {
        signal: AbortSignal.timeout(2000),
      });
      return response.ok;
    } catch {
      return false;
    }
  }

  /**
   * Connect to existing Chrome and check if NotebookLM session is valid
   */
  async authenticate(): Promise<AuthResult> {
    try {
      const wsEndpoint = await this.getWebSocketEndpoint();
      if (!wsEndpoint) {
        return {
          success: false,
          backend: this.name,
          message: 'Chrome not running with remote debugging. Start Chrome with: open -a "Google Chrome" --args --remote-debugging-port=9222',
        };
      }

      const browser = await chromium.connectOverCDP(wsEndpoint);
      const contexts = browser.contexts();

      if (contexts.length === 0) {
        await browser.close();
        return {
          success: false,
          backend: this.name,
          message: 'No browser contexts found. Please open Chrome and navigate to any page.',
        };
      }

      // Use the first (default) context
      const context = contexts[0];

      // Check if we have valid NotebookLM cookies
      const cookies = await context.cookies(this.config.notebookLmUrl);
      const hasAuthCookies = this.hasValidAuthCookies(cookies);

      if (!hasAuthCookies) {
        // Try to verify by navigating to NotebookLM
        const page = await context.newPage();
        try {
          await page.goto(this.config.notebookLmUrl, { timeout: 10000 });
          await page.waitForTimeout(2000);

          // Check if we're logged in (not on login page)
          const isLoggedIn = await this.checkLoginStatus(page);
          await page.close();

          if (!isLoggedIn) {
            return {
              success: false,
              backend: this.name,
              message: 'Not logged into NotebookLM. Please login in your Chrome browser first.',
              wsEndpoint,
            };
          }
        } catch (error) {
          await page.close();
          throw error;
        }
      }

      // Get all cookies for storage
      const allCookies = await context.cookies();
      const notebookCookies = allCookies.filter(c =>
        c.domain.includes('google.com') || c.domain.includes('notebooklm')
      );

      return {
        success: true,
        backend: this.name,
        message: 'Connected to existing Chrome session with valid NotebookLM login',
        cookies: this.convertCookies(notebookCookies),
        wsEndpoint,
      };
    } catch (error) {
      return {
        success: false,
        backend: this.name,
        message: `CDP connection failed: ${error instanceof Error ? error.message : String(error)}`,
      };
    }
  }

  /**
   * Get stored authentication (checks if CDP is available and has valid session)
   */
  async getStoredAuth(): Promise<AuthResult | null> {
    if (!(await this.isAvailable())) {
      return null;
    }
    const result = await this.authenticate();
    return result.success ? result : null;
  }

  /**
   * Clear auth - no-op for CDP as we don't control the browser session
   */
  async clearAuth(): Promise<void> {
    // Cannot clear auth from CDP - user must logout manually
    console.log('CDP backend: User must logout manually from Chrome');
  }

  /**
   * Get the WebSocket debugger URL from Chrome
   */
  private async getWebSocketEndpoint(): Promise<string | null> {
    try {
      const response = await fetch(`http://localhost:${this.config.cdpPort}/json/version`);
      const data = await response.json() as { webSocketDebuggerUrl?: string };
      return data.webSocketDebuggerUrl || null;
    } catch {
      return null;
    }
  }

  /**
   * Check if cookies contain valid auth tokens
   */
  private hasValidAuthCookies(cookies: Array<{ name: string; value: string; expires: number }>): boolean {
    // Look for Google auth cookies
    const authCookieNames = ['SID', 'HSID', 'SSID', 'APISID', 'SAPISID', '__Secure-1PSID'];
    const now = Date.now() / 1000;

    return cookies.some(cookie =>
      authCookieNames.includes(cookie.name) &&
      (cookie.expires === -1 || cookie.expires > now)
    );
  }

  /**
   * Check if the page shows logged-in state
   */
  private async checkLoginStatus(page: Page): Promise<boolean> {
    try {
      // Check for common logged-out indicators
      const loginButton = await page.$('text=Sign in');
      const accountButton = await page.$('[aria-label*="Account"]');

      // If we see a Sign in button and no account menu, we're logged out
      if (loginButton && !accountButton) {
        return false;
      }

      // Check URL - if redirected to accounts.google.com, not logged in
      const url = page.url();
      if (url.includes('accounts.google.com')) {
        return false;
      }

      return true;
    } catch {
      return false;
    }
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
 * Instructions for launching Chrome with remote debugging
 */
export function getCDPLaunchInstructions(): string {
  const platform = process.platform;

  if (platform === 'darwin') {
    return `
# macOS - Launch Chrome with remote debugging:
open -a "Google Chrome" --args --remote-debugging-port=9222

# Or create an alias in ~/.zshrc or ~/.bashrc:
alias chrome-debug='open -a "Google Chrome" --args --remote-debugging-port=9222'
`;
  } else if (platform === 'win32') {
    return `
# Windows - Launch Chrome with remote debugging:
"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222

# Or from PowerShell:
& "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222
`;
  } else {
    return `
# Linux - Launch Chrome with remote debugging:
google-chrome --remote-debugging-port=9222

# Or for Chromium:
chromium --remote-debugging-port=9222
`;
  }
}
