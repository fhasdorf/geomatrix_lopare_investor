"""Magic-Link access control. Phase 0: stub returns True for all (open access).
Phase 4 will implement HMAC-signed tokens, pitch-token URL param, session state."""

import streamlit as st


def has_access() -> bool:
    """Phase 0: always grant access. Phase 4 enforces real auth on gated pages."""
    return True


def require_access() -> None:
    """Call at top of gated pages. Phase 0: no-op."""
    if not has_access():
        st.warning("This area is gated. Request access on the Contact page.")
        st.stop()
