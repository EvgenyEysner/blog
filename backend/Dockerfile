FROM python:3.9 as base

# Move pipfiles to project.
RUN mkdir -p /app
WORKDIR /app

# Install required OS dependencies
RUN apt-get update &&  \
    apt-get install -y gettext && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pyhton dependencies
ADD Pipfile Pipfile.lock ./

RUN pip install -U pip pipenv

FROM base as prod-build-python

RUN pipenv install --system --verbose --deploy

FROM base as dev-build-python

RUN pipenv install --system --verbose --deploy --dev

### Dev image used for local development (bigger than prod image)
FROM dev-build-python as dev

COPY . /app/
WORKDIR /app

# Django-env expects this file to exist and prints warnings, but we use docker compose env vars.
RUN touch ./config/.env

# Set variable for celery
ENV COLUMNS=80

EXPOSE 8000

CMD ["./scripts/run_local.sh"]

### Prod image
FROM python:3.9-slim as prod
ENV PYTHONUNBUFFERED 1

# Install required OS dependencies
RUN apt-get update \
  && apt-get install -y \
  libxml2 \
  libssl1.1 \
  libcairo2 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libgdk-pixbuf2.0-0 \
  shared-mime-info \
  mime-support \
  postgresql \
  libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


COPY --from=prod-build-python /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=prod-build-python /usr/local/bin/ /usr/local/bin/

COPY . /app/
WORKDIR /app

# Django-env expects this file to exist and prints warnings, but we use docker compose env vars.
RUN touch ./config/.env

# Set variable for celery
ENV COLUMNS=80

EXPOSE 8000

CMD ["./scripts/run_backend.sh"]
