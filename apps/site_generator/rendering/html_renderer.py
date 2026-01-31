from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Dict, List, Any

from apps.site_generator.config.settings import SITE_BASE_URL, TEMPLATES_DIR, DISCIPLINES


class HTMLRenderer:

    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(TEMPLATES_DIR),
            autoescape=select_autoescape(["html", "xml"]),
        )

        # Фильтры для шаблона
        self.env.filters["match_date"] = self.format_match_date
        self.env.filters["match_time"] = self.format_match_time

    @staticmethod
    def _parse_datetime(value: str) -> datetime | None:
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception:
            return None

    @classmethod
    def format_match_date(cls, value: datetime | None) -> str:
        if not value:
            return ""
        return value.strftime("%d %b")

    @classmethod
    def format_match_time(cls, value: datetime | None) -> str:
        if not value:
            return ""
        return value.strftime("%H:%M")

    def render_matches_page(
            self,
            matches: List[Dict[str, Any]],
            day: str,
            discipline_key: str,
            return_string: bool = True,
    ):
        discipline_name = DISCIPLINES.get(discipline_key, discipline_key.capitalize())
        context = {
            "seo": {
                "title": f"{discipline_name} esports matches on {day.capitalize()}",
                "description": f"List of {discipline_name} matches on {day.capitalize()}",
                "keywords": f"esports, {discipline_name}, matches, tournaments",
            },
            "matches": matches,
            "day": day.capitalize(),
            "discipline": discipline_name,
            "discipline_key": discipline_key,
            "base_url": SITE_BASE_URL,
            "schema_org": self.generate_schema(matches),
        }
        template = self.env.get_template("matches.html")
        return template.render(**context)

    def render_home(self, disciplines: dict[str, str], return_string: bool = True) -> str:
        context = {
            "disciplines": disciplines,
            "seo": {
                "title": "Esports Disciplines",
                "description": "Select a discipline to view matches",
                "keywords": "esports, disciplines, matches",
            },
            "base_url": SITE_BASE_URL,
        }

        template = self.env.get_template("index.html")
        return template.render(**context)

    def generate_schema(self, matches_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        events = []

        for m in matches_list:
            opponents = [o.get("name") for o in m.get("opponents", [])]

            events.append({
                "@type": "SportsEvent",
                "name": m.get("name"),
                "startDate": m.get("begin_at"),
                "competitor": [
                    {"@type": "SportsTeam", "name": name}
                    for name in opponents
                ],
            })

        return {
            "@context": "https://schema.org",
            "@graph": events if events else [],
        }
