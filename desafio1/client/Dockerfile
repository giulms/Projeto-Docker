FROM python:3.13

COPY client.py /client.py

RUN pip install requests

EXPOSE 5000

CMD ["python", "/client.py"]