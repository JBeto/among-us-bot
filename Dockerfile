FROM python:3.8-buster

WORKDIR /among-us-bot
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY among/ among/
COPY assets/ assets/

# command to run on container start
ENTRYPOINT ["python3", "-m", "among"]