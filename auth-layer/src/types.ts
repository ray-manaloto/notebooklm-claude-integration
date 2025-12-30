/**
 * Authentication backend types for NotebookLM
 */

export type AuthBackendType =
  | 'cdp'           // Connect to existing Chrome via CDP
  | 'keychain'      // macOS Keychain stored cookies
  | 'persistent'    // Playwright persistent context
  | 'manual'        // Manual browser login (fallback)
  | 'chrome-mcp';   // Chrome DevTools MCP server

export interface AuthResult {
  success: boolean;
  backend: AuthBackendType;
  message: string;
  cookies?: Cookie[];
  wsEndpoint?: string;  // For CDP connections
  profilePath?: string; // For persistent context
}

export interface Cookie {
  name: string;
  value: string;
  domain: string;
  path: string;
  expires: number;
  httpOnly: boolean;
  secure: boolean;
  sameSite: 'Strict' | 'Lax' | 'None';
}

export interface AuthBackend {
  name: AuthBackendType;
  priority: number;
  isAvailable(): Promise<boolean>;
  authenticate(): Promise<AuthResult>;
  getStoredAuth(): Promise<AuthResult | null>;
  clearAuth(): Promise<void>;
}

export interface AuthConfig {
  /** Ordered list of backends to try (first available wins) */
  backends: AuthBackendType[];
  /** Chrome remote debugging port (for CDP) */
  cdpPort: number;
  /** Keychain service name */
  keychainService: string;
  /** Persistent profile directory */
  profileDir: string;
  /** NotebookLM URL to authenticate against */
  notebookLmUrl: string;
  /** Timeout for authentication attempts (ms) */
  timeout: number;
  /** Enable verbose logging */
  verbose: boolean;
}

export const DEFAULT_CONFIG: AuthConfig = {
  backends: ['cdp', 'keychain', 'persistent', 'manual'],
  cdpPort: 9222,
  keychainService: 'notebooklm-claude-auth',
  profileDir: '~/.notebooklm-auth/chrome-profile',
  notebookLmUrl: 'https://notebooklm.google.com',
  timeout: 60000,
  verbose: false,
};

export interface BrowserSession {
  type: 'cdp' | 'persistent' | 'fresh';
  browser: unknown; // Playwright Browser
  context: unknown; // Playwright BrowserContext
  page: unknown;    // Playwright Page
  close(): Promise<void>;
}
