FROM python:3.13

WORKDIR /code

ENV PYTHONPATH=/code

COPY ./requirements.txt /code/requirements.txt

COPY ./raw_data /code/raw_data

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./static /code/static

CMD ["fastapi", "run", "app/main.py", "--port", "80"]