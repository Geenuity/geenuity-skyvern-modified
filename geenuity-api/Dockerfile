FROM python:3.11

WORKDIR /app

COPY . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN pip install uvicorn fastapi requests python-dotenv

EXPOSE 9000

ENV PYTHONUNBUFFERED=1

CMD ["python", "__main__.py"]