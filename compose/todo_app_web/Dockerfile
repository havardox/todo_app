FROM python:3.11.6-bookworm AS base

ENV PYTHONUNBUFFERED=true \
  ### Python ###
  # Prevents python creating .pyc files.
  PYTHONDONTWRITEBYTECODE=true \
  \
  ### Project ###
  APP_HOME="/usr/src/app" \
  \
  ### PIP ###
  PIP_NO_CACHE_DIR=true \
  PIP_DISABLE_PIP_VERSION_CHECK=true \
  PIP_DEFAULT_TIMEOUT=100 \
  \
  ### Virtual environment ###
  VIRTUAL_ENV="/venv" \
  \
  ### Poetry ###
  # https://python-poetry.org/docs/configuration/#using-environment-variables
  POETRY_VERSION=1.4.2

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir -p "$VIRTUAL_ENV"

WORKDIR "$APP_HOME"

# COPY './compose/todo_app/entrypoint.sh' pyproject.toml "$APP_HOME"
COPY pyproject.toml "$APP_HOME"

RUN mkdir -p "$APP_HOME/todo_app" && touch "$APP_HOME/todo_app/__init__.py"

RUN apt-get update -qq \
  && apt-get install --no-install-recommends -y \
    build-essential \
    netcat-openbsd \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /usr/share/doc && rm -rf /usr/share/man \
  && pip install "poetry==$POETRY_VERSION" \
  && python -m venv "$VIRTUAL_ENV" \
  && poetry install --verbose --no-ansi \
  && apt-get autoremove --purge --yes \
    build-essential \
  && apt-get clean

ENTRYPOINT ["./compose/todo_app_web/entrypoint.sh"]

CMD ["python", "todo_app/main.py"]