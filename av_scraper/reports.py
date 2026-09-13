"""扫描结果导出：JSON / 文本 / CSV。"""

from __future__ import annotations

import csv
import datetime
import json
from pathlib import Path

from .scraper import ScrapeResult


def make_run_directory(base: str | Path) -> Path:
    """在 base 下按时间戳建立一次运行的输出目录。"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(base) / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def _to_dict(r: ScrapeResult) -> dict:
    return {
        "file_path": r.file_path,
        "filename": r.filename,
        "extracted_code": r.extracted_code,
        "status": r.status,
        "file_size": r.file_size,
    }


def save_json(results: list[ScrapeResult], path: Path) -> None:
    path.write_text(
        json.dumps([_to_dict(r) for r in results],
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def save_text_report(results: list[ScrapeResult], path: Path) -> None:
    total = len(results)
    extracted = sum(1 for r in results if r.is_extracted)
    ratio = extracted / total * 100 if total else 0

    lines = [
        "文件名刮削器处理报告",
        "=" * 50,
        f"处理时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"总文件数: {total}",
        f"成功提取: {extracted}",
        f"保持原样: {total - extracted}",
        f"提取率: {ratio:.1f}%",
        "",
        "=" * 50,
        "文件处理详情:",
        "-" * 50,
    ]
    for r in results:
        icon = "✓" if r.is_extracted else "○"
        lines.append(f"{icon} {r.filename} -> {r.extracted_code}")

    path.write_text("\n".join(lines), encoding="utf-8")


def save_csv(results: list[ScrapeResult], path: Path) -> None:
    extracted = sorted(
        (r for r in results if r.is_extracted),
        key=lambda r: r.extracted_code,
    )
    total = len(results)
    ratio = f"{len(extracted) / total * 100:.1f}%" if total else "0%"

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["原始文件名", "提取出的信息"])
        for r in extracted:
            writer.writerow([r.filename, r.extracted_code])
        writer.writerow([])
        writer.writerow(["统计信息"])
        writer.writerow(["总文件数", total])
        writer.writerow(["成功提取数", len(extracted)])
        writer.writerow(["提取率", ratio])
        writer.writerow(["生成时间",
                         datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])