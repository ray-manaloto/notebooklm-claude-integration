#!/usr/bin/env node
/**
 * nlm-auth CLI - Manage NotebookLM authentication
 *
 * Commands:
 *   status  - Show authentication status for all backends
 *   login   - Perform interactive login
 *   logout  - Clear all stored authentication
 *   cdp     - Show Chrome CDP setup instructions
 */

import { AuthManager } from './auth-manager.js';
import { getCDPLaunchInstructions } from './backends/cdp.js';
import { getKeychainStatus } from './backends/keychain.js';
import { getProfileStatus } from './backends/persistent.js';
import { DEFAULT_CONFIG } from './types.js';

const HELP = `
nlm-auth - NotebookLM Authentication Manager

USAGE:
  nlm-auth <command> [options]

COMMANDS:
  status    Show authentication status for all backends
  login     Perform interactive login (opens browser)
  logout    Clear all stored authentication
  cdp       Show Chrome CDP setup instructions
  check     Quick check if authenticated (exits 0 if yes, 1 if no)

OPTIONS:
  --verbose, -v    Enable verbose output
  --help, -h       Show this help message

AUTHENTICATION BACKENDS (tried in order):
  1. CDP        Connect to existing Chrome via remote debugging
  2. Keychain   Retrieve stored cookies from macOS Keychain
  3. Persistent Use Playwright persistent browser profile
  4. Manual     Interactive browser login (fallback)

EXAMPLES:
  # Check if already authenticated
  nlm-auth status

  # Login interactively
  nlm-auth login

  # Setup Chrome for CDP (best experience)
  nlm-auth cdp

  # Clear all auth and re-login
  nlm-auth logout && nlm-auth login
`;

async function main(): Promise<void> {
  const args = process.argv.slice(2);
  const command = args.find(a => !a.startsWith('-')) || 'status';
  const verbose = args.includes('--verbose') || args.includes('-v');

  if (args.includes('--help') || args.includes('-h')) {
    console.log(HELP);
    process.exit(0);
  }

  const manager = new AuthManager({ verbose });

  switch (command) {
    case 'status':
      await showStatus(manager);
      break;

    case 'login':
      await doLogin(manager);
      break;

    case 'logout':
      await doLogout(manager);
      break;

    case 'cdp':
      showCDPInstructions();
      break;

    case 'check':
      await quickCheck(manager);
      break;

    default:
      console.error(`Unknown command: ${command}`);
      console.log(HELP);
      process.exit(1);
  }
}

async function showStatus(manager: AuthManager): Promise<void> {
  console.log('\n🔐 NotebookLM Authentication Status\n');

  const status = await manager.getStatus();

  // Backend status table
  console.log('Backend Status:');
  console.log('─'.repeat(60));

  for (const backend of status.backends) {
    const icon = backend.hasAuth ? '✅' : backend.available ? '⚪' : '❌';
    const state = backend.hasAuth ? 'authenticated' : backend.available ? 'available' : 'unavailable';
    console.log(`  ${icon} ${backend.name.padEnd(12)} ${state.padEnd(15)} ${backend.details || ''}`);
  }

  console.log('─'.repeat(60));
  console.log(`\n${status.recommendation}\n`);

  // Additional details
  if (process.platform === 'darwin') {
    const keychainStatus = await getKeychainStatus(DEFAULT_CONFIG);
    if (keychainStatus.hasCookies) {
      console.log(`📦 Keychain: Cookies stored (saved: ${keychainStatus.savedAt})`);
    }
  }

  const profileStatus = await getProfileStatus(DEFAULT_CONFIG);
  if (profileStatus.hasState) {
    console.log(`📁 Profile: ${profileStatus.profilePath} (saved: ${profileStatus.savedAt})`);
  }
}

async function doLogin(manager: AuthManager): Promise<void> {
  console.log('\n🔐 NotebookLM Login\n');

  // First check if already authenticated
  const cookies = await manager.getCookies();
  if (cookies && cookies.length > 0) {
    console.log('Already authenticated. Use --force to re-login.');
    console.log('Or run: nlm-auth logout && nlm-auth login\n');

    const status = await manager.getStatus();
    console.log(status.recommendation);
    return;
  }

  // Try CDP first (best UX)
  console.log('Checking for running Chrome with remote debugging...');
  const cdpResult = await manager.authenticate();

  if (cdpResult.success) {
    console.log(`\n✅ ${cdpResult.message}`);
    console.log('\nYou can now use NotebookLM with Claude!\n');
    return;
  }

  // Fall back to interactive login
  console.log('Chrome not available or not logged into NotebookLM.');
  console.log('Falling back to interactive login...\n');

  const result = await manager.interactiveLogin();

  if (result.success) {
    console.log(`\n✅ ${result.message}`);
    console.log('\nYou can now use NotebookLM with Claude!\n');
  } else {
    console.error(`\n❌ ${result.message}`);
    process.exit(1);
  }
}

async function doLogout(manager: AuthManager): Promise<void> {
  console.log('\n🔐 Clearing NotebookLM Authentication\n');

  await manager.clearAuth();

  console.log('✅ Cleared all stored authentication:');
  console.log('   • macOS Keychain cookies');
  console.log('   • Persistent browser profile state');
  console.log('\nRun `nlm-auth login` to re-authenticate.\n');
}

function showCDPInstructions(): void {
  console.log('\n🔗 Chrome Remote Debugging Setup\n');
  console.log('For the best experience, run Chrome with remote debugging enabled.');
  console.log('This lets the auth layer connect to your existing logged-in session.\n');

  console.log(getCDPLaunchInstructions());

  console.log('\nBENEFITS:');
  console.log('  • No separate login needed - uses your existing session');
  console.log('  • Faster authentication - no browser automation');
  console.log('  • Works with your existing Chrome extensions');
  console.log('\nNOTE: Only one instance of Chrome can use a remote debugging port at a time.');
  console.log('Close other Chrome instances before starting with this flag.\n');
}

async function quickCheck(manager: AuthManager): Promise<void> {
  const cookies = await manager.getCookies();
  if (cookies && cookies.length > 0) {
    console.log('authenticated');
    process.exit(0);
  } else {
    console.log('not authenticated');
    process.exit(1);
  }
}

// Run
main().catch(error => {
  console.error('Error:', error instanceof Error ? error.message : String(error));
  process.exit(1);
});
