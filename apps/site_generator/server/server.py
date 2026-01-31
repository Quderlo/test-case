from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, send_from_directory
from apps.site_generator.infrastructure.pandascore.client import PandaScoreClient
from apps.site_generator.services.matches_service import MatchesService
from apps.site_generator.rendering.html_renderer import HTMLRenderer
from apps.site_generator.config.settings import DISCIPLINES, MEDIA_STATIC


app = Flask(__name__, static_folder=str(MEDIA_STATIC), static_url_path="/static")
client = PandaScoreClient()
service = MatchesService()
renderer = HTMLRenderer()


@app.route("/")
def home():
    return renderer.render_home(DISCIPLINES, return_string=True)

@app.route("/<discipline>/<day>")
def matches_page(discipline: str, day: str):
    if discipline not in DISCIPLINES:
        return "Дисциплина не найдена", 404
    if day not in ["yesterday", "today", "tomorrow"]:
        return "Страница не найдена", 404

    # Получаем матчи за 3 дня одним запросом
    now = datetime.now(client.tz)
    start = now - timedelta(days=1)
    end = now + timedelta(days=2)
    all_matches = client.get_matches_for_range(start, end, discipline)
    grouped = service.group_matches_by_day(all_matches)
    prepared = service.prepare_grouped_matches(grouped).get(day, [])

    return renderer.render_matches_page(prepared, day, discipline)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
