# /notebook-auth - Manage NotebookLM authentication

Manage your Google NotebookLM authentication and browser session.

## Usage

```
/notebook-auth status
/notebook-auth setup
/notebook-auth reset
/notebook-auth clear
```

## Commands

### Check authentication status
```
/notebook-auth status
```
Returns whether you're authenticated and session expiry.

### Setup authentication (first time)
```
/notebook-auth setup
```
Opens Chrome for Google login. Credentials are saved locally for future use.

### Reset session
```
/notebook-auth reset
```
Clears saved session and forces re-authentication on next use.

### Clear all browser data
```
/notebook-auth clear
```
Removes all browser state, auth tokens, and session data.
Use this if experiencing Chrome crashes or login issues.

## Notes

- Authentication data stored in `~/.claude/skills/notebooklm/data/browser_state/`
- Uses real Chrome profile for persistent login
- Session typically lasts 30+ days
- Safe to use - credentials never leave your machine

## Security

- All data stored locally
- No credentials sent to external servers
- Chrome runs locally on your machine
- Consider using a dedicated Google account
