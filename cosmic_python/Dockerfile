FROM python:3.9-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./src ./src
COPY ./tests ./tests
COPY pyproject.toml pyproject.toml
COPY .flaskenv .flaskenv
COPY README.md README.md

RUN pip install -e .

CMD ["gunicorn", "-w", "1", "-b", "127.0.0.1:5005", "api:app"]