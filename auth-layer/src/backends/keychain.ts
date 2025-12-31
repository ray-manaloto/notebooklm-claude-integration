/**
 * Keychain Backend - Store/retrieve cookies from macOS Keychain
 *
 * Uses the macOS `security` CLI to securely store NotebookLM session
 * cookies in the system keychain. These cookies can be injected into
 * a fresh Playwright browser to restore the session.
 */

import { execFile } from 'child_process';
import { promisify } from 'util';
import type { AuthBackend, AuthResult, AuthConfig, Cookie } from '../types.js';

const execFileAsync = promisify(execFile);

export class KeychainAuthBackend implements AuthBackend {
  name = 'keychain' as const;
  priority = 2;

  constructor(private config: AuthConfig) {}

  /**
   * Check if we're on macOS and keychain is accessible
   */
  async isAvailable(): Promise<boolean> {
    if (process.platform !== 'darwin') {
      return false;
    }

    try {
      // Check if security command is available
      await execFileAsync('which', ['security']);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Authenticate by retrieving stored cookies from keychain
   */
  async authenticate(): Promise<AuthResult> {
    const stored = await this.getStoredAuth();
    if (stored) {
      return stored;
    }

    return {
      success: false,
      backend: this.name,
      message: 'No stored credentials in keychain. Run authentication with another backend first, then save cookies.',
    };
  }

  /**
   * Get stored authentication from keychain
   */
  async getStoredAuth(): Promise<AuthResult | null> {
    try {
      const cookiesJson = await this.getFromKeychain('cookies');
      if (!cookiesJson) {
        return null;
      }

      const cookies: Cookie[] = JSON.parse(cookiesJson);

      // Validate cookies haven't expired
      const now = Date.now() / 1000;
      const validCookies = cookies.filter(c => c.expires === -1 || c.expires > now);

      if (validCookies.length === 0) {
        await this.clearAuth();
        return null;
      }

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
        message: 'Retrieved valid cookies from macOS Keychain',
        cookies: validCookies,
      };
    } catch (error) {
      if (this.config.verbose) {
        console.error('Keychain retrieval error:', error);
      }
      return null;
    }
  }

  /**
   * Store cookies in keychain after successful authentication
   */
  async storeCookies(cookies: Cookie[]): Promise<void> {
    const cookiesJson = JSON.stringify(cookies);
    await this.saveToKeychain('cookies', cookiesJson);

    // Also store a timestamp for debugging
    await this.saveToKeychain('saved-at', new Date().toISOString());
  }

  /**
   * Clear all stored authentication from keychain
   */
  async clearAuth(): Promise<void> {
    await this.deleteFromKeychain('cookies');
    await this.deleteFromKeychain('saved-at');
  }

  /**
   * Save a value to macOS Keychain using execFile (safe from injection)
   */
  private async saveToKeychain(key: string, value: string): Promise<void> {
    const service = this.config.keychainService;
    const account = `${process.env.USER || 'user'}-${key}`;
    const trustedApps = this.getTrustedApps();
    const trustedArgs = trustedApps.flatMap(app => ['-T', app]);

    // Delete existing entry first (ignore errors)
    try {
      await execFileAsync('security', [
        'delete-generic-password',
        '-s', service,
        '-a', account
      ]);
    } catch {
      // Ignore - entry may not exist
    }

    // Add new entry using execFile with arguments array (safe from injection)
    await execFileAsync('security', [
      'add-generic-password',
      '-s', service,
      '-a', account,
      '-w', value,
      ...trustedArgs
    ]);
  }

  /**
   * Get a value from macOS Keychain using execFile (safe from injection)
   */
  private async getFromKeychain(key: string): Promise<string | null> {
    const service = this.config.keychainService;
    const account = `${process.env.USER || 'user'}-${key}`;

    try {
      const { stdout } = await execFileAsync('security', [
        'find-generic-password',
        '-s', service,
        '-a', account,
        '-w'
      ]);
      return stdout.trim();
    } catch (error) {
      const stderr = (error as { stderr?: string }).stderr ?? '';
      const stderrText = String(stderr);
      if (stderrText.includes('User interaction is not allowed') || stderrText.includes('interaction not allowed')) {
        if (this.config.verbose) {
          console.warn('Keychain access requires user interaction; skipping keychain backend.');
        }
        return null;
      }
      return null;
    }
  }

  /**
   * Delete a value from macOS Keychain using execFile (safe from injection)
   */
  private async deleteFromKeychain(key: string): Promise<void> {
    const service = this.config.keychainService;
    const account = `${process.env.USER || 'user'}-${key}`;

    try {
      await execFileAsync('security', [
        'delete-generic-password',
        '-s', service,
        '-a', account
      ]);
    } catch {
      // Ignore - entry may not exist
    }
  }

  /**
   * Allowlist apps that can read the keychain item without UI prompts.
   */
  private getTrustedApps(): string[] {
    const trusted = new Set<string>();
    if (process.execPath) {
      trusted.add(process.execPath);
    }
    trusted.add('/usr/bin/security');
    return Array.from(trusted);
  }
}

/**
 * Helper to get keychain status
 */
export async function getKeychainStatus(config: AuthConfig): Promise<{
  available: boolean;
  hasCookies: boolean;
  savedAt: string | null;
}> {
  if (process.platform !== 'darwin') {
    return { available: false, hasCookies: false, savedAt: null };
  }

  const service = config.keychainService;
  const user = process.env.USER || 'user';

  try {
    let savedAt: string | null = null;
    let hasCookies = false;

    try {
      const { stdout } = await execFileAsync('security', [
        'find-generic-password',
        '-s', service,
        '-a', `${user}-saved-at`,
        '-w'
      ]);
      savedAt = stdout.trim() || null;
    } catch {
      // Entry doesn't exist
    }

    try {
      const { stdout } = await execFileAsync('security', [
        'find-generic-password',
        '-s', service,
        '-a', `${user}-cookies`,
        '-w'
      ]);
      hasCookies = stdout.trim().length > 0;
    } catch {
      // Entry doesn't exist
    }

    return {
      available: true,
      hasCookies,
      savedAt,
    };
  } catch {
    return { available: true, hasCookies: false, savedAt: null };
  }
}
