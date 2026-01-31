from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import Any, Dict, List

from apps.site_generator.config.settings import TIMEZONE, PLACEHOLDER_LOGO


class MatchesService:
    def __init__(self, timezone: str = TIMEZONE):
        self.tz = ZoneInfo(timezone)

    def group_matches_by_day(self, matches: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
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
        begin_str = match.get("begin_at")
        match_dt = None
        if begin_str:
            try:
                match_dt = datetime.fromisoformat(begin_str.replace("Z", "+00:00")).astimezone(self.tz)
            except Exception:
                pass

        # Приводим тип матча к читаемому виду
        match_type = match.get("match_type")
        number_of_games = match.get("number_of_games")
        human_match_type = ""
        if match_type:
            human_match_type = match_type.replace("_", " ").title()
            if number_of_games:
                human_match_type += f" - {number_of_games} game" + ("s" if number_of_games > 1 else "")

        status = match.get("status")
        human_status = status.capitalize() if status else ""

        # Обработка команд
        opponents_list = []
        for o in match.get("opponents", []):
            opponent = o.get("opponent")
            name = opponent.get("name") if opponent and opponent.get("name") else "TBD"
            image_url = opponent.get("image_url") if opponent and opponent.get("image_url") else PLACEHOLDER_LOGO
            opponents_list.append({
                "name": name,
                "image_url": image_url,
            })

        # Если вообще нет соперников
        while len(opponents_list) < 2:
            opponents_list.append({"name": "TBD", "image_url": PLACEHOLDER_LOGO})

        return {
            "id": match.get("id"),
            "name": match.get("name"),
            "league": match.get("league", {}).get("name") if match.get("league") else "",
            "serie": match.get("serie", {}).get("full_name") if match.get("serie") else "",
            "videogame": match.get("videogame", {}).get("name") if match.get("videogame") else "",
            "match_type": human_match_type,
            "status": human_status,
            "begin_at_dt": match_dt,
            "opponents": opponents_list,
            "results": match.get("results", []),
            "tournament": match.get("tournament", {}).get("name") if match.get("tournament") else "",
            "streams": match.get("streams", []),
            "live_url": match.get("live_url"),
        }

    def prepare_grouped_matches(self, grouped_matches: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        result: Dict[str, List[Dict[str, Any]]] = {}
        for key, matches in grouped_matches.items():
            result[key] = [self.prepare_match_for_template(m) for m in matches]
        return result
