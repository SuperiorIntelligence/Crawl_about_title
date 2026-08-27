"""پیکربندی و ابزارهای هسته."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "settings.yaml"
CACHE_DIR = ROOT / "data" / "cache"
RESULTS_PATH = ROOT / "data" / "results.json"


def load_settings(path: Path | None = None) -> dict[str, Any]:
    """خواندن تنظیمات YAML پروژه."""
    cfg = path or CONFIG_PATH
    with cfg.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


class RateLimiter:
    """محدودکنندهٔ سادهٔ نرخ درخواست به‌ازای هر host."""

    def __init__(self, min_interval_sec: float) -> None:
        self.min_interval = min_interval_sec
        self._last: dict[str, float] = {}

    def wait(self, host: str) -> None:
        """در صورت نیاز صبر می‌کند تا فاصلهٔ مجاز رعایت شود."""
        now = time.monotonic()
        last = self._last.get(host, 0.0)
        delay = self.min_interval - (now - last)
        if delay > 0:
            time.sleep(delay)
        self._last[host] = time.monotonic()


class FileCache:
    """کش فایل‌محور برای پاسخ‌های HTTP / نتایج."""

    def __init__(self, directory: Path | None = None, ttl_sec: int = 3600) -> None:
        self.directory = directory or CACHE_DIR
        self.ttl_sec = ttl_sec
        self.directory.mkdir(parents=True, exist_ok=True)

    def _key_path(self, key: str) -> Path:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        return self.directory / f"{digest}.json"

    def get(self, key: str) -> Any | None:
        """خواندن مقدار کش اگر منقضی نشده باشد."""
        path = self._key_path(key)
        if not path.exists():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
        if time.time() - payload.get("ts", 0) > self.ttl_sec:
            return None
        return payload.get("data")

    def set(self, key: str, data: Any) -> None:
        """ذخیرهٔ مقدار در کش."""
        path = self._key_path(key)
        path.write_text(
            json.dumps({"ts": time.time(), "data": data}, ensure_ascii=False),
            encoding="utf-8",
        )


def save_results(report_dict: dict[str, Any]) -> Path:
    """ذخیرهٔ آخرین گزارش در data/results.json."""
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(
        json.dumps(report_dict, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    return RESULTS_PATH


def load_results() -> dict[str, Any] | None:
    """خواندن آخرین گزارش ذخیره‌شده."""
    if not RESULTS_PATH.exists():
        return None
    return json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
