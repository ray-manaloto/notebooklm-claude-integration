/**
 * NotebookLM Auth Layer
 *
 * Multi-backend authentication for NotebookLM MCP server
 *
 * @example
 * ```typescript
 * import { getAuthManager } from 'notebooklm-auth-layer';
 *
 * const manager = getAuthManager();
 * const result = await manager.authenticate();
 *
 * if (result.success) {
 *   console.log('Authenticated via', result.backend);
 *   // Use result.cookies to inject into browser
 * }
 * ```
 */

// Core exports
export { AuthManager, getAuthManager } from './auth-manager.js';
export type {
  AuthBackend,
  AuthBackendType,
  AuthConfig,
  AuthResult,
  BrowserSession,
  Cookie,
} from './types.js';
export { DEFAULT_CONFIG } from './types.js';

// Backend exports
export {
  CDPAuthBackend,
  getCDPLaunchInstructions,
  KeychainAuthBackend,
  getKeychainStatus,
  PersistentAuthBackend,
  getProfileStatus,
} from './backends/index.js';

/**
 * Quick helper to check if authenticated
 */
export async function isAuthenticated(): Promise<boolean> {
  const { getAuthManager } = await import('./auth-manager.js');
  const manager = getAuthManager();
  const cookies = await manager.getCookies();
  return cookies !== null && cookies.length > 0;
}

/**
 * Quick helper to get cookies for browser injection
 */
export async function getAuthCookies(): Promise<Array<{
  name: string;
  value: string;
  domain: string;
  path: string;
  expires: number;
  httpOnly: boolean;
  secure: boolean;
  sameSite: 'Strict' | 'Lax' | 'None';
}> | null> {
  const { getAuthManager } = await import('./auth-manager.js');
  const manager = getAuthManager();
  return manager.getCookies();
}
