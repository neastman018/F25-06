FROM python:3.10-slim
# Set the working directory
WORKDIR /backend

RUN pip install poetry==1.6.1


# Copy the requirements file
COPY  pyproject.toml poetry.lock ./

RUN poetry install


# Want to copy this last so it only changes 
COPY ./app ./app

# Expose the port
EXPOSE 4000