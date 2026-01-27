FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
RUN pip install --upgrade pip
RUN pip install .

COPY . /app

EXPOSE 5000

CMD ["python", "-m", "apps.site_generator.server.server"]
