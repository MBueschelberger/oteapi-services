# Open Translation Environment (OTE) API

## Run in Docker

### Development target

The development target will allow for automatic reloading when source code changes.
This requires that the local directory is bind-mounted using the `-v` or `--volume` argument.
To build and run the development target from the command line:

```shell
docker build --rm -f Dockerfile \
    --label "ontotrans.oteapi=development" \
    --target development \
    -t "ontotrans/oteapi-development:latest" .
```

### Production target

The production target will not reload itself on code change and will run a predictable version of the code on port 80.
Also you might want to use a named container with the `--restart=always` option to ensure that the container is restarted indefinitely regardless of the exit status.
To build and run the production target from the command line:

```shell
docker build --rm -f Dockerfile \
    --label "ontotrans.oteapi=production" \
    --target production \
    -t "ontotrans/oteapi:latest" .

```

### Run redis

Redis with persistance needs to run as a prerequisite to starting oteapi.
Redis needs to share the same network as oteapi.

```shell
docker network create -d bridge otenet
docker volume create redis-persist
docker run \
    --detach \
    --name redis \
    --volume redis-persist:/data \
    --network otenet \
    redis:latest
```

### Run oteapi (development)

Run the services by attaching to the otenet network and set the environmental variables for connecting to Redis.

```shell
docker run \
    --rm \
    --network otenet \
    --detach \
    --volume ${PWD}:/app \
    --publish 8080:8080 \
    --env OTEAPI_REDIS_TYPE=redis \
    --env OTEAPI_REDIS_HOST=redis \
    --env OTEAPI_REDIS_PORT=6379 \
    ontotrans/oteapi-development:latest
```

Open the following URL in a browser [http://localhost:8080/redoc](http://localhost:8080/redoc).

### Run oteapi (production)

Run the services by attaching to the otenet network and set the environmental variables for connecting to Redis.

```shell
docker run \
    --rm \
    --network otenet \
    --detach \
    --publish 80:8080 \
    --env OTEAPI_REDIS_TYPE=redis \
    --env OTEAPI_REDIS_HOST=redis \
    --env OTEAPI_REDIS_PORT=6379 \
    ontotrans/oteapi:latest
```

Open the following URL in a browser [http://localhost:80/redoc](http://localhost:80/redoc).

### Run the Atmoz SFTP Server

To test the data access via SFTP, the atmoz sftp-server can be run:

```shell
docker volume create sftpdrive
PASSWORD="Insert your user password here" docker run \
    --detach \
    --network=otenet \
    --volume sftpdrive:${HOME}/download \
    --publish 2222:22 \
    atmoz/sftp ${USER}:${PASSWORD}:1001
```

For production, SSH public key authentication is preferred.

## Run with Docker Compose

Prepare the Docker Compose system by running:

```shell
docker-compose pull  # Pull the latest images
docker-compose build  # Build the central OTE service (from Dockerfile)
```

Now one can simply run:

```shell
docker-compose up -d  # Run the OTE Services (detached)
```

Note that default values will be used if certain environment variables are not present.
To inspect which environment variables can be specified, please inspect the [Docker Compose file](docker-compose.yml).
