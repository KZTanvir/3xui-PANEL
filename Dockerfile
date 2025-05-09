FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

WORKDIR /code

COPY app/ /code/app/
COPY run.py /code/run.py

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /code
USER appuser

EXPOSE 5000

# Important: tell gunicorn to change directory to /code so it can find run.py
CMD ["gunicorn", "--chdir", "/code", "--bind", "0.0.0.0:5000", "run:app"]
