FROM python:3.10.9-buster as base

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH=$PATH:/root/.local/share/pypoetry/venv/bin/

COPY pyproject.toml poetry.toml /app/

WORKDIR /app

RUN poetry install --no-root --no-dev


FROM base as production

COPY todo_app /app/todo_app/

EXPOSE 8000

ENTRYPOINT poetry run gunicorn --bind=0.0.0.0 "todo_app.app:create_app()"


FROM base as development

RUN poetry install --no-root

ENV FLASK_DEBUG=1

EXPOSE 5000

ENTRYPOINT poetry run flask run --host=0.0.0.0


FROM base as test

RUN poetry install --no-root

COPY todo_app /app/todo_app/

ENTRYPOINT ["poetry", "run", "pytest"]