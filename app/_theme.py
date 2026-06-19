"""Theme injection. Phase 0: stub. Phase 2: full CSS for glassmorphism, hero, cards."""

import streamlit as st


def inject_theme() -> None:
    """Inject custom CSS. Phase 0 = no-op placeholder."""
    # Phase 2 will inject Google Fonts (Space Grotesk, Inter, JetBrains Mono),
    # hero background, glassmorphism card styles, CTA button polish.
    st.markdown(
        "<!-- theme CSS placeholder — Phase 2 -->",
        unsafe_allow_html=True,
    )
