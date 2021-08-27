FROM python:3.8

RUN pip install -U pip poetry

WORKDIR /usr/app

COPY ./pyproject.toml /usr/app/pyproject.toml

RUN poetry install

COPY ./hostthedocs/ /usr/app/hostthedocs/
ADD ./runserver.py /usr/app/runserver.py

ENV HTD_HOST="0.0.0.0" HTD_PORT=5000

EXPOSE 5000

CMD ["poetry", "run", "python", "runserver.py"]
