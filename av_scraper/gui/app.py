"""主窗口。"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import ttk

from ..config import AppConfig
from .config_tab import ConfigTab
from .move_tab import MoveTab
from .scan_tab import ScanTab


class App(tk.Tk):
    def __init__(self, config_path: Path):
        super().__init__()
        self.title("文件刮削与整理工具")
        self.geometry("1180x820")
        self.minsize(960, 640)

        self.config_path = config_path
        self.app_config = AppConfig.load(config_path)

        self._build()

    def _build(self) -> None:
        try:
            ttk.Style(self).theme_use("vista")
        except tk.TclError:
            pass

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=6, pady=6)

        self.scan_tab = ScanTab(nb, self)
        self.move_tab = MoveTab(nb, self)
        self.config_tab = ConfigTab(nb, self)

        nb.add(self.scan_tab, text="① 扫描")
        nb.add(self.move_tab, text="② 移动")
        nb.add(self.config_tab, text="③ 配置")

        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(
            self, textvariable=self.status_var, anchor="w",
            relief="sunken", padding=(6, 2),
        ).pack(fill="x", side="bottom")

    def set_status(self, text: str) -> None:
        self.status_var.set(text)

    # 供 ConfigTab 保存后调用，让其他页读取新配置
    def refresh_from_config(self) -> None:
        self.scan_tab.sync_from_config()
        self.move_tab.sync_from_config()