FROM python:3.11

WORKDIR /app

RUN pip install poetry==1.4.2

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-interaction --no-cache

WORKDIR /app/src

COPY src .

EXPOSE 8000
ENTRYPOINT ["poetry", "run", "python", "main.py"]
