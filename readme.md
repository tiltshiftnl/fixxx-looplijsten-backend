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

## Retreiving fixtures
You can download a fixtures with the 'DOWNLOAD JSON FIXTURE' button for the team settings from an looplijst enviroment if you have superuser rights for this enviroment:
For acceptance: https://acc.api.top.amsterdam.nl/admin/planner/
For production: https://api.top.amsterdam.nl/admin/planner/

## Loading fixtures
You can load fixtures (.json) for the team settings in your local development database:
```bash
docker-compose run --rm api python manage.py loaddata apps/planner/fixtures/[filename.json]
```

## Accessing the API documentation
You can access the documentation at:
http://localhost:8000/api/v1/swagger/

## Generating an access token
When the LOCAL_DEVELOPMENT_AUTHENTICATION environment variable is set to True, you can gain access easily in the Swagger documentation by executing the /api/v1/oidc-authenticate/ POST request.
You can use the 'access' token in the response:
Click on the 'Authorize' button in the top right corner of the page, and enter the given access token.
This allows you to execute the API endpoints in the page.

## Adding pre-commit hooks
You can add pre-commit hooks for checking and cleaning up your changes:
```
bash install.sh
```

You can also run the following command to ensure all files adhere to coding conventions:
```
bash cleanup.sh
```
This will autoformat your code, sort your imports and fix or find overal problems.

The Github actions will use the same bash script to check if the code in the pull requests follows the formatting and style conventions.

## Coding conventions and style
The project uses [Black](https://github.com/psf/black) for formatting and [Flake8](https://pypi.org/project/flake8/) for linting.

# Testing
## Running unit tests
Unit tests can be run using the following command:
```
docker-compose run --rm api python manage.py test
```

## Unit test in pull requests
Unit tests are part of the Github action workflows, and will be run when a pull request is made. This ensures tests are maintained and increases maintainability and dependability of automatic pull requests.

## Health check
A path is available for checking the health of the running application, and all its connected services.
The overview of this status can be found on the following path: {application_url}/health
To improve reliability, the health checks should be expanded for each essential service that is added to the application. For more on how to expand the health checks, read the [Django Healh Check documentation](https://github.com/KristianOellegaard/django-health-check).
