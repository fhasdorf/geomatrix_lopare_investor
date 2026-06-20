"""Language toggle for the Lopare Investor app.

Session-state based, app-wide. Default language is English. The toggle is
rendered in the sidebar and persists across page navigation.
"""

from __future__ import annotations

from typing import Literal

import streamlit as st

Lang = Literal["en", "de"]

DEFAULT_LANG: Lang = "en"

LABELS: dict[Lang, dict[str, str]] = {
    "en": {
        "language_label": "Language",
        "en_option": "🇬🇧 English",
        "de_option": "🇩🇪 Deutsch",
    },
    "de": {
        "language_label": "Sprache",
        "en_option": "🇬🇧 English",
        "de_option": "🇩🇪 Deutsch",
    },
}


def init_lang() -> None:
    """Idempotent — call at the top of every page."""
    if "lang" not in st.session_state:
        st.session_state.lang = DEFAULT_LANG


def get_lang() -> Lang:
    """Returns the currently active language."""
    init_lang()
    return st.session_state.lang


def render_lang_toggle() -> None:
    """Render the sidebar language toggle. Call once per page in the sidebar."""
    init_lang()
    current = get_lang()
    labels = LABELS[current]

    options = ["en", "de"]
    option_labels = {"en": labels["en_option"], "de": labels["de_option"]}

    selected = st.sidebar.radio(
        labels["language_label"],
        options,
        format_func=lambda x: option_labels[x],
        index=options.index(current),
        horizontal=True,
        key="lang_radio",
    )
    if selected != current:
        st.session_state.lang = selected
        st.rerun()
