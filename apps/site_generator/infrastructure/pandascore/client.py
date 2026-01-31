from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import List, Dict, Any

import requests

from apps.site_generator.config.settings import (
    PANDASCORE_API_TOKEN,
    TIMEZONE,
    DATE_FORMAT,
    PANDASCORE_API_URL,
    DISCIPLINES,
)


class PandaScoreClient:
    """Клиент для работы с PandaScore API с учетом таймзоны."""

    def __init__(self, token: str = PANDASCORE_API_TOKEN, timezone: str = TIMEZONE):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        self.tz = ZoneInfo(timezone)

    def _get(self, endpoint: str, params: dict = None) -> List[Dict[str, Any]]:
        url = f"{PANDASCORE_API_URL}/{endpoint}"
        try:
            resp = self.session.get(url, params=params, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            print(f"[PandaScoreClient] Error fetching {url}: {e}")
            return []

    def get_matches_for_range(self, start: datetime, end: datetime, discipline: str = "dota2") -> List[Dict[str, Any]]:
        """Получаем все матчи за указанный диапазон дат с учетом таймзоны клиента."""
        from apps.site_generator.config.settings import DISCIPLINES

        if discipline.lower() not in DISCIPLINES:
            discipline = "dota2"

        params = {
            "range[begin_at]": f"{start.strftime(DATE_FORMAT)},{end.strftime(DATE_FORMAT)}",
            "sort": "begin_at",
        }
        endpoint = f"{discipline.lower()}/matches"
        return self._get(endpoint, params=params)

    def get_matches_yesterday_today_tomorrow(
        self,
        discipline: str = "dota2",
    ) -> List[Dict[str, Any]]:
        now = datetime.now(self.tz)

        start = datetime(
            now.year,
            now.month,
            now.day,
            0,
            0,
            tzinfo=self.tz,
        ) - timedelta(days=1)

        end = start + timedelta(days=3)

        return self.get_matches_range(start, end, discipline)
