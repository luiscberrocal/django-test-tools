FROM python:3.6.3
ENV PYTHONUNBUFFERED 1

RUN groupadd -r django \
    && useradd -r -g django django

#dockerfile instructions
COPY . /app/

COPY ./compose/django/start-dev.sh /app/example/start-dev.sh
RUN sed -i 's/\r//' /app/example/start-dev.sh
RUN chmod +x /app/example/start-dev.sh && chown django /app/example/start-dev.sh

WORKDIR /app/example



RUN pip install -r requirements.txt


RUN chown -R django /app

USER django
