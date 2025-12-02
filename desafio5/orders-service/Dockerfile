FROM python:3.13

WORKDIR /app

RUN pip install Flask

COPY app.py .

EXPOSE 5001

CMD ["python", "app.py"]