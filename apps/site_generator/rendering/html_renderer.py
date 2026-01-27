from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Dict, List, Any
from apps.site_generator.config.settings import SITE_BASE_URL, TEMPLATES_DIR


class HTMLRenderer:

    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(TEMPLATES_DIR),
            autoescape=select_autoescape(["html", "xml"])
        )
        self.env.filters['format_datetime'] = self.format_datetime

    @staticmethod
    def format_datetime(value: str, fmt="%Y-%m-%d %H:%M UTC") -> str:
        try:
            dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
            return dt.strftime(fmt)
        except Exception:
            return value

    def render_matches_page(
        self,
        matches: List[Dict[str, Any]],
        day: str,
        discipline: str,
        return_string: bool = True,
    ) -> str:
        context = {
            "seo": {
                "title": f"{discipline.upper()} esports matches on {day.capitalize()}",
                "description": f"List of {discipline.upper()} matches on {day.capitalize()}",
                "keywords": f"esports, {discipline}, matches, tournaments",
            },
            "matches": matches,
            "day": day.capitalize(),
            "discipline": discipline.upper(),
            "base_url": SITE_BASE_URL,
            "schema_org": self.generate_schema(matches, day),
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

    def generate_schema(self, matches_list: list[dict], day: str) -> dict:
        events = []
        for m in matches_list:
            opponents = [o.get("name") for o in m.get("opponents", [])]
            events.append({
                "@type": "SportsEvent",
                "name": m.get("name"),
                "startDate": m.get("begin_at"),
                "location": {"@type": "Place", "name": m.get("league", "")},
                "competitor": [{"@type": "SportsTeam", "name": n} for n in opponents],
            })
        return {"@context": "https://schema.org", "@graph": events if events else [{}]}

