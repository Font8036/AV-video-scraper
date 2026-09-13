"""GUI 入口：python -m av_scraper"""

from __future__ import annotations

from .gui.app import App
from .paths import config_path


def main() -> None:
    App(config_path()).mainloop()


if __name__ == "__main__":
    main()