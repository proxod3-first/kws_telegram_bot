FROM python:3.10-slim

RUN apt update
RUN pip install --upgrade pip

WORKDIR /home/kws
COPY . .

RUN python3 -m pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "/home/kws/main.py"]