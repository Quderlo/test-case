from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Any, Dict, List

from apps.site_generator.config.settings import TIMEZONE


class MatchesService:
    """Сервис для обработки матчей и подготовки к рендеру."""

    def __init__(self, timezone: str = TIMEZONE):
        self.tz = ZoneInfo(timezone)

    def group_matches_by_day(self, matches: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Группирует список матчей по дням: 'yesterday', 'today', 'tomorrow'.
        matches — список JSON объектов с API PandaScore
        """
        now = datetime.now(self.tz)
        days = {
            "yesterday": now - timedelta(days=1),
            "today": now,
            "tomorrow": now + timedelta(days=1),
        }

        grouped: Dict[str, List[Dict[str, Any]]] = {"yesterday": [], "today": [], "tomorrow": []}

        for match in matches:
            begin_str = match.get("begin_at")
            if not begin_str:
                continue

            try:
                match_dt = datetime.fromisoformat(begin_str.replace("Z", "+00:00")).astimezone(self.tz)
            except ValueError:
                continue

            for key, day in days.items():
                if match_dt.date() == day.date():
                    grouped[key].append(match)
                    break

        return grouped

    def prepare_match_for_template(self, match: Dict[str, Any]) -> Dict[str, Any]:
        """
        Подготавливает матч для рендеринга в шаблоне HTML/SSR.
        Можно добавлять дополнительные поля для SEO/schema.org.
        """
        return {
            "id": match.get("id"),
            "name": match.get("name"),
            "league": match.get("league", {}).get("name") if match.get("league") else "",
            "begin_at": match.get("begin_at"),
            "status": match.get("status"),
            "opponents": [
                {
                    "name": o.get("opponent", {}).get("name") if o.get("opponent") else "",
                    "image_url": o.get("opponent", {}).get("image_url") if o.get("opponent") else "",
                }
                for o in match.get("opponents", [])
            ],
        }

    def prepare_grouped_matches(self, grouped_matches: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Применяет prepare_match_for_template ко всем матчам.
        """
        result: Dict[str, List[Dict[str, Any]]] = {}
        for key, matches in grouped_matches.items():
            result[key] = [self.prepare_match_for_template(m) for m in matches]
        return result
