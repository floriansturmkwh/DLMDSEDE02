FROM python:latest

# working directory
WORKDIR /app

# dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# scripts to folder
COPY . /app

CMD ["python", "./main.py"]