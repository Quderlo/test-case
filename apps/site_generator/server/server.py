from datetime import datetime

from flask import Flask
from apps.site_generator.infrastructure.pandascore.client import PandaScoreClient
from apps.site_generator.services.matches_service import MatchesService
from apps.site_generator.rendering.html_renderer import HTMLRenderer
from apps.site_generator.config.settings import DISCIPLINES

app = Flask(__name__)
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

    # Получаем матчи динамически
    if day == "yesterday":
        matches = client.get_matches_yesterday(discipline)
    elif day == "today":
        matches = client.get_matches_today(discipline)
    else:
        matches = client.get_matches_tomorrow(discipline)

    # Подготовка для шаблона
    prepared = service.prepare_grouped_matches({"matches": matches}).get("matches", matches)
    html = renderer.render_matches_page(prepared, day, discipline, return_string=True)
    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
