#Flask server image
FROM python:3.9.2
#Setup working directory
WORKDIR /usr/src/app
#Copy all files into container
COPY . .

#Install the essential libraries on alpine 
RUN pip3 install --upgrade pip
# Install the requirements to run flask endpoint and SQAM.
RUN pip3 install -r requirements.txt
#Run the flask backend
CMD ["python3", "-u", "main.py"]