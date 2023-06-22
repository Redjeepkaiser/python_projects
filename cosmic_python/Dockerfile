FROM python:3.9-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./src .
COPY ./tests .
COPY pyproject.toml pyproject.toml
COPY .flaskenv .flaskenv

RUN pip3 install -e .

CMD ["gunicorn", "-w", "4", "-b", "127.0.0.1:5005", "api:app"]