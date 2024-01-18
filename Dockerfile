# Pull base image
FROM python:3.8
LABEL maintainer="vikas"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install virtualenv
RUN virtualenv env --python=python3.8
RUN . env/bin/activate
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=core/server.py

# Run the initial migrations
RUN flask db upgrade -d core/migrations/

# Expose the port on which the app will run
EXPOSE 7755

# Set executable permissions
RUN chmod +x /app/run.sh

# Run scripts when the container launches
CMD ["bash","run.sh"]