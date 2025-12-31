# NotebookLM Auth Layer

Multi-backend authentication layer for NotebookLM MCP server. Provides seamless authentication by trying multiple backends in priority order.

## Features

- **CDP Backend** - Connect to existing Chrome browser (best UX if already logged in)
- **Keychain Backend** - Securely store/retrieve cookies from macOS Keychain
- **Persistent Context** - Playwright persistent browser profile for session storage
- **Automatic Fallback** - Tries backends in order until one succeeds

## Quick Start

```bash
# Install dependencies
cd auth-layer
npm install

# Build
npm run build

# Check authentication status
npm run cli status

# Login (opens browser if needed)
npm run cli login

# For best experience, run Chrome with debugging first
npm run cli cdp  # Shows setup instructions
```

## Authentication Backends

### 1. CDP (Chrome DevTools Protocol) - Priority 1

Connects to an existing Chrome browser via remote debugging. **Best UX** because it uses your already logged-in session.

```bash
# Start Chrome with remote debugging
open -a "Google Chrome" --args --remote-debugging-port=9222

# The auth layer will automatically detect and use this session
```

### 2. Keychain (macOS only) - Priority 2

Stores authentication cookies securely in macOS Keychain. Fast and works headlessly.

```bash
# Cookies are automatically saved to keychain after successful login
# To check keychain status:
security find-generic-password -s "notebooklm-claude-auth" -a "$USER-cookies" -w
```

### 3. Persistent Context - Priority 3

Uses Playwright's persistent browser profile to maintain session across restarts.

Profile location: `~/.notebooklm-auth/chrome-profile/`

### 4. Manual Login - Fallback

Opens a browser window for interactive Google login if all other backends fail.

## CLI Commands

```bash
nlm-auth status    # Show authentication status for all backends
nlm-auth login     # Perform interactive login
nlm-auth logout    # Clear all stored authentication
nlm-auth cdp       # Show Chrome CDP setup instructions
nlm-auth check     # Quick check (exit code 0 if authenticated)
```

## Programmatic Usage

```typescript
import { getAuthManager, isAuthenticated, getAuthCookies } from 'notebooklm-auth-layer';

// Quick check
if (await isAuthenticated()) {
  console.log('Ready to use NotebookLM');
}

// Full control
const manager = getAuthManager({
  verbose: true,
  cdpPort: 9222,
});

const result = await manager.authenticate();
if (result.success) {
  console.log('Backend used:', result.backend);
  console.log('Cookies:', result.cookies?.length);
}

// Get cookies for injection
const cookies = await getAuthCookies();
if (cookies) {
  await browserContext.addCookies(cookies);
}
```

## Configuration

```typescript
import { AuthConfig, DEFAULT_CONFIG } from 'notebooklm-auth-layer';

const config: Partial<AuthConfig> = {
  // Order of backends to try
  backends: ['cdp', 'keychain', 'persistent', 'manual'],

  // Chrome remote debugging port
  cdpPort: 9222,

  // macOS Keychain service name
  keychainService: 'notebooklm-claude-auth',

  // Persistent profile directory
  profileDir: '~/.notebooklm-auth/chrome-profile',

  // Authentication timeout (ms)
  timeout: 60000,

  // Enable verbose logging
  verbose: false,
};

const manager = getAuthManager(config);
```

## Security

- **CDP**: Uses your existing Chrome session - no credentials stored
- **Keychain**: Cookies encrypted by macOS Keychain (requires login password)
- **Persistent**: Cookies stored in local profile directory
- **No credentials logged**: Only session cookies are handled, never passwords

## Troubleshooting

### Chrome not detected for CDP

```bash
# Ensure Chrome is started with remote debugging:
open -a "Google Chrome" --args --remote-debugging-port=9222

# Check if debugging is enabled:
curl http://localhost:9222/json/version
```

### Keychain permission denied

```bash
# Check if the service exists:
security find-generic-password -s "notebooklm-claude-auth"

# If prompted, allow access in the Keychain Access app
```

If you see “User interaction is not allowed” in headless runs, clear the existing
keychain entry and re-login so the tool can re-save cookies with a trusted-app
allowlist:

```bash
nlm-auth logout
nlm-auth login
```

### Session expired

```bash
# Clear all auth and re-login:
nlm-auth logout
nlm-auth login
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      AuthManager                             │
├─────────────────────────────────────────────────────────────┤
│  authenticate() → tries backends in priority order          │
│  getStatus()    → returns status of all backends            │
│  getCookies()   → returns cookies from first available      │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  CDP Backend  │   │Keychain Backend│   │Persistent     │
│  (Priority 1) │   │  (Priority 2)  │   │  (Priority 3) │
├───────────────┤   ├───────────────┤   ├───────────────┤
│ Chrome ws://  │   │ security CLI  │   │ Playwright    │
│ localhost:9222│   │ add/find/del  │   │ userDataDir   │
└───────────────┘   └───────────────┘   └───────────────┘
```

## License

MIT
