FROM python:3.12
WORKDIR /app
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0
RUN pip install -r requirements.txt
COPY . /app
CMD ["python", "app.py"]