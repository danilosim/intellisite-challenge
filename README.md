# Intellisite Challenge

This whole challenge is containerised, it's using MongoDB as the database, and FastAPI as the webframework

## Implemented Features

- Indexer microservice with Kafka Consumer to read messages from `intellisite.detections` and alert about suspicious vehicles using a Kafka Producer that post messages to `intellisite.alerts`.
- API:
  - Swagger docs accessible at the root endpoint (`localhost:8080` when running locally)
  - Superuser creation using CLI script
  - Users with permissions based on roles (`superadmin` and `client`)
  - User creation at `POST /users` (only available for `superadmin` users)
  - Login at `POST /auth/token` with the required username and password as form fields
  - Refresh token at `GET /auth/refresh` which requires the user to be currently authenticated
  - Check current user at `GET /users/me`
  - Alerts (Server Sent Events) at `GET /alerts` reading the `intellisite.alerts` topic. (available for all users to be easily tested in the browser, but you can check the commented line at `api/routers/alerts.py` with the code necessary to make it only accessible by authenticated users)
  - Detections at `GET /detections` (only available for authenticated users)
  - Stats at `GET /stats` (only available for authenticated users)
  - MongoDB UI to easily check that the data at `http://localhost:5001/` when running the project locally

## Setup

- Create docker network (only the first time)

```bash
docker network create intellisite
```

- Spin up the local single-node Kafka cluster (will run in the background):

```bash
$ docker-compose -f docker/docker-compose.kafka.yml up -d
```

- Check the cluster is up and running (wait for "started" to show up):

```bash
$ docker-compose -f docker/docker-compose.kafka.yml logs -f broker | grep "started"
```

- Start the detections producer (will run in the background):

```bash
$ docker-compose -f docker/docker-compose.producer.yml up -d
```

- Start the indexer service:

```bash
$ docker-compose -f docker/docker-compose.indexer.yml up -d
```

- Start the API service:

```bash
$ docker-compose -f docker/docker-compose.api.yml up -d
```

- Create superuser (only the first time):

```bash
docker exec -it docker-api python create_superadmin.py --username user --password pass1234
```

- Test endpoints using provided Postman collection at `postman_collection.json`
  - Remember to use the login endpoint first, and then pass the received token in the headers in every following request
- Test alert endpoint using the browser at `localhost:8080/alerts`
- Check mongo data at `localhost:5001`

## Teardown

To stop the detections producer:

```bash
$ docker-compose -f docker/docker-compose.producer.yml down
```

To stop the Kafka cluster (use `down` instead to also remove contents of the topics):

```bash
$ docker-compose -f docker/docker-compose.kafka.yml stop
```

To remove the Docker network:

```bash
$ docker network rm intelliste
```

To stop remaining services use:

```bash
$ docker-compose -f docker/docker-compose.indexer.yml down
$ docker-compose -f docker/docker-compose.api.yml down
$ docker-compose -f docker/docker-compose.indexer.yml down
```

## Pending improvements

- Improve error handling (use more specific errors and exceptions)
- Improve project structure (separate API endpoints from service logic)
- Add tests for endpoints and utils
- Improve user login and authentication with a permission schema on resources instead of using roles
- Improve DB and Request/Response data models
- Improve password hashing, use salt, etc.
