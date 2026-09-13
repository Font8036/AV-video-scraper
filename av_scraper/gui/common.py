"""GUI 通用工具。"""

from __future__ import annotations

import logging
import queue
import tkinter.ttk as ttk

class QueueLogHandler(logging.Handler):
    """把日志记录推入 queue，由主线程消费后写入 Text 控件。"""

    def __init__(self, q: queue.Queue):
        super().__init__()
        self.q = q

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.q.put(self.format(record))
        except Exception:
            self.handleError(record)


def human_size(n: float) -> str:
    n = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{int(n)} B" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

def remember_dir(history: list[str], new_dir: str, limit: int) -> list[str]:
    """把 new_dir 放到历史首位，去重，截断到 limit。"""
    new_dir = (new_dir or "").strip()
    if not new_dir:
        return list(history)
    deduped = [new_dir] + [d for d in history if d != new_dir]
    return deduped[: max(1, int(limit))]


def make_dir_combobox(parent, textvariable, width: int = 40) -> "ttk.Combobox":
    """点击展开下拉的 Combobox。"""

    cb = ttk.Combobox(parent, textvariable=textvariable, width=width)
    # 点击整行都能展开（不止是右侧箭头）
    cb.bind("<Button-1>",
            lambda e: cb.after_idle(lambda: cb.event_generate("<Down>")))
    return cb