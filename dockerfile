FROM python:slim-buster

COPY . safety_assessment

WORKDIR .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install -r safety_assessment/src/requirements.txt
RUN pip install jupyterlab matplotlib

ENV PYTHONPATH "${PYTHONPATH}:/safety_assessment/"

CMD ["bash", "/safety_assessment/helper-scripts/start.sh"]
