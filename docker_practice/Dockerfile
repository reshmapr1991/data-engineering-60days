# start from official Python image
FROM python:3.11-slim

# set working directory inside container
WORKDIR /app

# copy requirements first (for caching)
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy your code
COPY etl.py .

# run the script when container starts
CMD ["python", "etl.py"]
