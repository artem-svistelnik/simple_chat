FROM python:3.11

ENV PYTHONUNBUFFERED=1
ENV VENV "/venv"
ENV PATH "${VENV}/bin:${PATH}"
ENV PYTHONPATH "${PYTHONPATH}:/opt/backend"

WORKDIR /opt/backend

COPY pyproject.toml poetry.lock ./

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . .
