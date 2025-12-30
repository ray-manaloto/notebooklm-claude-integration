/**
 * AuthManager - Orchestrates multiple authentication backends
 *
 * Tries backends in priority order:
 * 1. CDP (connect to existing Chrome) - best UX if Chrome is running
 * 2. Keychain (stored cookies) - fast, secure, works headless
 * 3. Persistent (browser profile) - reliable fallback
 * 4. Manual (interactive login) - last resort
 */

import type { AuthBackend, AuthResult, AuthConfig, Cookie, AuthBackendType } from './types.js';
import { DEFAULT_CONFIG } from './types.js';
import { CDPAuthBackend } from './backends/cdp.js';
import { KeychainAuthBackend } from './backends/keychain.js';
import { PersistentAuthBackend } from './backends/persistent.js';

export class AuthManager {
  private backends: Map<AuthBackendType, AuthBackend> = new Map();
  private config: AuthConfig;

  constructor(config: Partial<AuthConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.initializeBackends();
  }

  /**
   * Initialize all authentication backends
   */
  private initializeBackends(): void {
    this.backends.set('cdp', new CDPAuthBackend(this.config));
    this.backends.set('keychain', new KeychainAuthBackend(this.config));
    this.backends.set('persistent', new PersistentAuthBackend(this.config));
  }

  /**
   * Get authentication using the best available backend
   *
   * Tries backends in configured order, returns first successful auth
   */
  async authenticate(): Promise<AuthResult> {
    const results: Array<{ backend: AuthBackendType; available: boolean; result?: AuthResult }> = [];

    for (const backendType of this.config.backends) {
      const backend = this.backends.get(backendType);
      if (!backend) continue;

      const available = await backend.isAvailable();
      if (!available) {
        results.push({ backend: backendType, available: false });
        continue;
      }

      if (this.config.verbose) {
        console.log(`Trying ${backendType} backend...`);
      }

      // First try to get stored auth (fast path)
      const stored = await backend.getStoredAuth();
      if (stored?.success) {
        if (this.config.verbose) {
          console.log(`${backendType}: Found valid stored auth`);
        }
        return stored;
      }

      // Try full authentication
      const result = await backend.authenticate();
      results.push({ backend: backendType, available: true, result });

      if (result.success) {
        // If we got cookies from a non-keychain backend, save to keychain
        if (backendType !== 'keychain' && result.cookies) {
          await this.saveCookiesToKeychain(result.cookies);
        }
        return result;
      }
    }

    // All backends failed - return summary
    return {
      success: false,
      backend: 'manual',
      message: this.formatFailureMessage(results),
    };
  }

  /**
   * Get status of all authentication backends
   */
  async getStatus(): Promise<{
    backends: Array<{
      name: AuthBackendType;
      available: boolean;
      hasAuth: boolean;
      details?: string;
    }>;
    recommendation: string;
  }> {
    const statuses: Array<{
      name: AuthBackendType;
      available: boolean;
      hasAuth: boolean;
      details?: string;
    }> = [];

    for (const backendType of this.config.backends) {
      const backend = this.backends.get(backendType);
      if (!backend) continue;

      const available = await backend.isAvailable();
      let hasAuth = false;
      let details: string | undefined;

      if (available) {
        const stored = await backend.getStoredAuth();
        hasAuth = stored?.success || false;
        details = stored?.message;
      } else {
        details = this.getUnavailableReason(backendType);
      }

      statuses.push({ name: backendType, available, hasAuth, details });
    }

    // Generate recommendation
    let recommendation: string;
    const hasAnyAuth = statuses.some(s => s.hasAuth);

    if (hasAnyAuth) {
      const authBackend = statuses.find(s => s.hasAuth);
      recommendation = `Ready to use NotebookLM (authenticated via ${authBackend?.name})`;
    } else {
      const cdpStatus = statuses.find(s => s.name === 'cdp');
      if (cdpStatus?.available) {
        recommendation = 'Login to NotebookLM in your Chrome browser, then retry';
      } else {
        recommendation = 'Run `nlm-auth login` to authenticate via browser';
      }
    }

    return { backends: statuses, recommendation };
  }

  /**
   * Force re-authentication (clears all stored auth)
   */
  async reauthenticate(): Promise<AuthResult> {
    // Clear all stored auth
    for (const backend of this.backends.values()) {
      await backend.clearAuth();
    }

    // Try CDP first (if Chrome is running with valid session)
    const cdpBackend = this.backends.get('cdp') as CDPAuthBackend;
    if (await cdpBackend.isAvailable()) {
      const result = await cdpBackend.authenticate();
      if (result.success && result.cookies) {
        await this.saveCookiesToKeychain(result.cookies);
        return result;
      }
    }

    // Fall back to persistent context login
    return this.interactiveLogin();
  }

  /**
   * Perform interactive login using persistent context
   */
  async interactiveLogin(): Promise<AuthResult> {
    const persistent = this.backends.get('persistent') as PersistentAuthBackend;

    console.log('\n🔐 Opening browser for NotebookLM login...');
    console.log('Please complete the Google login in the browser window.\n');

    const { page, saveAndClose } = await persistent.launchForLogin();

    // Wait for user to login (check periodically)
    const maxWait = this.config.timeout;
    const checkInterval = 2000;
    let elapsed = 0;

    while (elapsed < maxWait) {
      await new Promise(resolve => setTimeout(resolve, checkInterval));
      elapsed += checkInterval;

      // Check if we're logged in by looking at the URL and cookies
      const url = page.url();

      // If we're on NotebookLM (not login page), we might be logged in
      if (url.includes('notebooklm.google.com') && !url.includes('accounts.google.com')) {
        // Additional check - look for logged-in UI elements
        const accountButton = await page.$('[aria-label*="Account"]');
        if (accountButton) {
          console.log('✅ Login detected! Saving session...');
          const result = await saveAndClose();

          if (result.success && result.cookies) {
            await this.saveCookiesToKeychain(result.cookies);
          }

          return result;
        }
      }

      // Print progress
      if (elapsed % 10000 === 0) {
        console.log(`⏳ Waiting for login... (${Math.round((maxWait - elapsed) / 1000)}s remaining)`);
      }
    }

    // Timeout - try to save anyway
    console.log('⚠️ Timeout reached. Attempting to save current state...');
    return saveAndClose();
  }

  /**
   * Clear all stored authentication
   */
  async clearAuth(): Promise<void> {
    for (const backend of this.backends.values()) {
      await backend.clearAuth();
    }
  }

  /**
   * Get cookies for injecting into a browser session
   */
  async getCookies(): Promise<Cookie[] | null> {
    for (const backendType of this.config.backends) {
      const backend = this.backends.get(backendType);
      if (!backend) continue;

      if (!(await backend.isAvailable())) continue;

      const stored = await backend.getStoredAuth();
      if (stored?.success && stored.cookies) {
        return stored.cookies;
      }
    }
    return null;
  }

  /**
   * Save cookies to keychain for future use
   */
  private async saveCookiesToKeychain(cookies: Cookie[]): Promise<void> {
    const keychain = this.backends.get('keychain') as KeychainAuthBackend;
    if (await keychain.isAvailable()) {
      await keychain.storeCookies(cookies);
      if (this.config.verbose) {
        console.log('Saved cookies to macOS Keychain');
      }
    }
  }

  /**
   * Format failure message from all backend results
   */
  private formatFailureMessage(results: Array<{
    backend: AuthBackendType;
    available: boolean;
    result?: AuthResult;
  }>): string {
    const lines = ['Authentication failed. Backend status:'];

    for (const { backend, available, result } of results) {
      if (!available) {
        lines.push(`  • ${backend}: not available`);
      } else if (result) {
        lines.push(`  • ${backend}: ${result.message}`);
      }
    }

    lines.push('');
    lines.push('Try: nlm-auth login');

    return lines.join('\n');
  }

  /**
   * Get reason why a backend is unavailable
   */
  private getUnavailableReason(backend: AuthBackendType): string {
    switch (backend) {
      case 'cdp':
        return 'Chrome not running with --remote-debugging-port=9222';
      case 'keychain':
        return 'Not on macOS or keychain not accessible';
      case 'persistent':
        return 'Persistent context always available';
      case 'manual':
        return 'Manual login always available';
      default:
        return 'Unknown backend';
    }
  }
}

// Export singleton for convenience
let defaultManager: AuthManager | null = null;

export function getAuthManager(config?: Partial<AuthConfig>): AuthManager {
  if (!defaultManager || config) {
    defaultManager = new AuthManager(config);
  }
  return defaultManager;
}
