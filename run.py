"""顶层入口：直接 python run.py 或双击运行。"""

import sys
from pathlib import Path

# 保证能 import 到 av_scraper 包，无论从哪里双击
sys.path.insert(0, str(Path(__file__).resolve().parent))

from av_scraper.__main__ import main

if __name__ == "__main__":
    main()