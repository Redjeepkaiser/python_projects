FROM python:3.9-bookworm

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./src ./src
COPY ./tests ./tests
COPY pyproject.toml pyproject.toml
COPY .flaskenv .flaskenv
COPY README.md README.md

RUN pip install -e .

CMD ["flask", "run"]