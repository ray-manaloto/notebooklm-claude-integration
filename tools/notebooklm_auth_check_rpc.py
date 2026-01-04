"""Check NotebookLM auth cookies via a lightweight request."""

from __future__ import annotations

import json
import logging
import os
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def _load_cookie_header(auth_file: Path) -> str:
    """Load the cookie header from the auth file."""
    data = json.loads(auth_file.read_text())
    cookies = data.get("cookies", {})
    if not cookies:
        message = "no cookies found in auth file"
        raise ValueError(message)
    return "; ".join(f"{k}={v}" for k, v in cookies.items())


def _check_auth(cookie_header: str, url: str) -> str:
    """Send an auth probe request and return the final URL."""
    parsed = urlparse(url)
    if parsed.scheme != "https":
        message = f"unsupported URL scheme: {parsed.scheme}"
        raise ValueError(message)
    req = urllib.request.Request(url)  # noqa: S310
    req.add_header("Cookie", cookie_header)
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:  # noqa: S310
        return resp.geturl()


def main() -> int:
    """Run the auth check for the configured NotebookLM URL."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    auth_file = Path(
        os.environ.get("AUTH_FILE", "~/.notebooklm-mcp/auth.json"),
    ).expanduser()
    url = os.environ.get("NOTEBOOKLM_URL", "https://notebooklm.google.com/")

    if not auth_file.exists() or auth_file.stat().st_size == 0:
        logger.error("Auth file not found at %s.", auth_file)
        logger.error("Run: notebooklm-mcp-auth --file")
        return 1

    try:
        cookie_header = _load_cookie_header(auth_file)
    except (json.JSONDecodeError, ValueError, OSError):
        logger.exception("Failed to load cookies from %s.", auth_file)
        return 1

    try:
        final_url = _check_auth(cookie_header, url)
    except (OSError, ValueError):
        logger.exception("Auth check failed.")
        return 1

    if "accounts.google.com" in final_url:
        logger.error("Auth appears expired (redirected to login).")
        logger.error("Re-auth with: notebooklm-mcp-auth --file")
        return 1

    logger.info("Auth looks valid (no login redirect).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
