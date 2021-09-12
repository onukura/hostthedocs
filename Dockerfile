FROM python:3.8

RUN pip install -U pip poetry

WORKDIR /usr/app

COPY ./pyproject.toml /usr/app/pyproject.toml

RUN poetry install

COPY ./hostthedocs/ /usr/app/hostthedocs/

EXPOSE 8080

CMD ["poetry", "run", "gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "hostthedocs:app", "--bind", ":8080"]