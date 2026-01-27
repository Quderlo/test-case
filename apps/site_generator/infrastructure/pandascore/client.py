from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Any, Dict

import requests

from apps.site_generator.config.settings import PANDASCORE_API_TOKEN, TIMEZONE, DATE_FORMAT, PANDASCORE_API_URL


class PandaScoreClient:
    """Клиент для работы с PandaScore API."""

    def __init__(self, token: str = PANDASCORE_API_TOKEN, timezone: str = TIMEZONE):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        self.tz = ZoneInfo(timezone)

    def _get(self, endpoint: str, params: dict = None) -> list[dict]:
        url = f"{PANDASCORE_API_URL}/{endpoint}"
        try:
            resp = self.session.get(url, params=params, timeout=5)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            print(f"[PandaScoreClient] Error fetching {url}: {e}")
            return []

    # Добавляем аргумент discipline
    def get_matches_for_day(self, day: datetime, discipline: str = "dota2") -> list[dict]:
        from apps.site_generator.config.settings import DISCIPLINES  # импорт внутри метода

        if discipline.lower() not in DISCIPLINES:
            discipline = "dota2"

        start = datetime(day.year, day.month, day.day, 0, 0, tzinfo=self.tz)
        end = start + timedelta(days=1)
        params = {
            "range[begin_at]": f"{start.strftime(DATE_FORMAT)},{end.strftime(DATE_FORMAT)}",
            "sort": "begin_at",
        }

        endpoint = f"{discipline.lower()}/matches"

        return self._get(endpoint, params=params)

    def get_matches_yesterday(self, discipline: str = "dota2"):
        day = datetime.now(self.tz) - timedelta(days=1)
        return self.get_matches_for_day(day, discipline)

    def get_matches_today(self, discipline: str = "dota2"):
        day = datetime.now(self.tz)
        return self.get_matches_for_day(day, discipline)

    def get_matches_tomorrow(self, discipline: str = "dota2"):
        day = datetime.now(self.tz) + timedelta(days=1)
        return self.get_matches_for_day(day, discipline)

