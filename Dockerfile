FROM python:3.10.9-buster

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Update path variables
ENV PATH=$PATH:/root/.local/share/pypoetry/venv/bin/

# Copy across toml file for poetry install
# Needs trailing slash to consider app as directory rather than file
COPY pyproject.toml poetry.toml /app/

# Change the working directory
WORKDIR /app

# Run the poetry installer
RUN poetry install

# Copy across application code
COPY todo_app /app/todo_app/

# Copy across env templte file
COPY .env.template /app/

# Clone .env from the template
RUN cp .env.template .env

EXPOSE 8000

# Define an entrypoint and default launch command
# ENTRYPOINT poetry run flask run --host=0.0.0.0
ENTRYPOINT poetry run gunicorn --bind=0.0.0.0 "todo_app.app:create_app()"

# We'll want to bind mount the folder that contains my code (todo_app) into the container
# That will keep it in sync when running the dev container, and maybe enable hot reloading
# Can run it using: docker run --env-file .env -p 8000:8000 todo-app
# But this is using my local env file, we need to supply them instead!