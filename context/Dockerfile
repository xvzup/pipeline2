# Use an official Python runtime as a parent image
FROM fokkodriesprong/docker-pyspark:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Update pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Download data
RUN curl -LO https://raw.githubusercontent.com/xvzup/pipeline2/master/context/message.csv 

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python" , "sparkTest.py"]