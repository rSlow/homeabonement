# Pull base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_DIR=/user/app

# Create and set work directory called `app`
RUN mkdir -p /code
WORKDIR $APP_DIR

# Install librares for mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
python3-dev

# Install dependencies
COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

# Copy local project
COPY . $APP_DIR

# Run entrypoint
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh