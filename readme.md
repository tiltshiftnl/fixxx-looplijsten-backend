# fixxx-looplijsten
plannen en inzien van efficiëntere looplijsten, bedoeld voor toezichthouders en handhavers van illegaal vakantieverhuur.

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)

# Steps For Local Development

## Build:
```bash
docker-compose build
```

## Build with hitkans (optional):
If you want to run fraud prediction scoring (hitkans) you can run the build with an optional argument:
```bash
docker-compose build --build-arg INTEGRALE_AANPAK_ONDERMIJNING_PERSONAL_ACCESS_TOKEN=GITLAB_PERSONAL_ACCESS_TOKEN_HERE
```
Replace the GITLAB_PERSONAL_ACCESS_TOKEN_HERE with your private token.
This token can be acquired through the private Amsterdam gitlab woonfraude repository.

## Starting the development server:
Start the dev server for local development:
```bash
docker-compose up
```

## Importing an SQL dump
Once you've built your Docker images and have started the development server (see previous steps), you can import an SQL dump.

To load local *bwv* dumps into the local *bwv* database:
```bash
bwv_db/import.sh </path/to/local/dir/with/dumps>
```

Make sure you are pointing to a directory, not the sql dump file itself.

## Creating a superuser:
```bash
docker-compose run --rm api python manage.py createsuperuser
```
A superuser can be used to access the Django backend

## Accessing the Django admin and adding users:
In order to generate lists you need at least 2 other users.
You can add other users easily through the Django admin.
Navigate to http://localhost:8000/admin and sign in using the superuser you just created.
Once you're in the admin, you can click on "add" in the User section to create new users.

## Bypassing Grip and using local development authentication:
It's possible to bypass Grip authentication when running the project locally.
To do so, make sure the LOCAL_DEVELOPMENT_AUTHENTICATION flag is set to True in docker-compose.yml.

# Running commands
Run a command inside the docker container:

```bash
docker-compose run --rm api [command]
```

Running migrations:
```bash
docker-compose run --rm api python manage.py migrate
```
