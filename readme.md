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
docker-compose build --build-arg INTEGRALE_AANPAK_ONDERMIJNING_CREDS={GITLAB_ACCESS_TOKEN_HERE}
```
Replace the {GITLAB_ACCESS_TOKEN_HERE} access token with your private token. 
This token can be acquired through the private Amsterdam gitlab woonfraude repository.

Run a command inside the docker container:

```bash
docker-compose run --rm api [command]
```

Running migrations:
```bash
docker-compose run --rm api python manage.py migrate
```

To load local *bwv* dumps into the local *bwv* database:
```bash
bwv_db/import.sh </path/to/local/dir/with/dumps>
```

Creating a superuser:
```bash
docker-compose run --rm api python manage.py createsuperuser
```
A superuser can be used to access the Django backend


Frontend steps when pulling new backend code:
```bash
docker-compose build
docker-compose run --rm api python manage.py migrate
docker-compose run --rm api python manage.py populate
docker-compose up
