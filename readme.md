# fixxx-looplijsten
plannen en inzien van efficiëntere looplijsten, bedoeld voor toezichthouders en handhavers van illegaal vakantieverhuur.

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

To rebuild (for example, when dependencies are added requirements.txt):
```bash
docker-compose build
```

Run a command inside the docker container:

```bash
docker-compose run --rm api [command]
```

Running migrations:
```bash
docker-compose run --rm api python manage.py migrate
```

To load some initial mock data run:
```bash
docker-compose run --rm api python manage.py loaddata /app/datasets/initial_data.json
```

To dump data into a mock data JSON, run:
```bash
run --rm api python manage.py dumpdata --format=json users itinerary > REPLACE_WITH_FILE_NAME.json
```

Creating a superuser:
```bash
docker-compose run --rm api python manage.py createsuperuser
```
A superuser can be used to access the Django backend