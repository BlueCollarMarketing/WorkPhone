from __future__ import annotations

from typing import Any


def run_demo_session() -> list[dict[str, Any]]:
    """Ring -> answer -> greet -> idle end (lab)."""
    return [
        {"t": "0.0s", "state": "ring", "detail": "Inbound invite received"},
        {"t": "1.2s", "state": "answer", "detail": "Session answered on forward path"},
        {"t": "1.5s", "state": "greet", "detail": "Trade-neutral greeting played"},
        {"t": "12.0s", "state": "active", "detail": "Caller speech / NLU turn"},
        {"t": "45.0s", "state": "fallback", "detail": "Voicemail offer if human unreachable"},
        {"t": "60.0s", "state": "end", "detail": "Idle end; session torn down"},
    ]
