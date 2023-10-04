FROM python:3.10.12

USER root
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true

ENV POSTGRES_HOST postgres
ENV REDIS_CACHE redis://redis:6379/

RUN mkdir /app
COPY . /app
COPY poetry.lock /app
COPY pyproject.toml /app

WORKDIR /app

RUN apt update && \
    apt-get install -y build-essential python3-pip  && \
    apt-get install -y libpq-dev python3-dev graphviz && \
    apt-get install -y unixodbc-dev && \
    apt-get install -y iputils-ping && \
    apt-get install -y default-libmysqlclient-dev && \
    apt-get install -y --no-install-recommends unixodbc-dev && \
    apt install libaio1 && \
    python -m pip install --upgrade pip && \
    pip install pkginfo virtualenv poetry  && \
    poetry config virtualenvs.create false

RUN poetry install --no-root --no-dev -vvv


#RUN pip install --no-cache-dir b2m.core b2m.client b2m.ingestion.executor b2m.dataframe.csv b2m.dataframe.excel b2m.datasource.s3 b2m.datasource.sql b2m.api b2m.ml.automl b2m.mljar.supervised b2m.ml.bigdata -i http://odin:asgard_2021.@3.67.172.47/simple/ --trusted-host 3.67.172.47

WORKDIR /app

CMD ["/app/docker-entrypoint.sh"]
