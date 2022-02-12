FROM python:3.9-alpine3.14

RUN apk update && apk upgrade && apk add curl
RUN curl -o poetry.py -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py && python poetry.py -y
ENV PATH /root/.poetry/bin:$PATH
RUN poetry config virtualenvs.create true && poetry config virtualenvs.in-project true

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install

COPY app app

EXPOSE 8080

CMD ["poetry", "run", "python", "-m", "app"]