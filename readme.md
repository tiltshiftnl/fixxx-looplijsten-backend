# fixxx-looplijsten
plannen en inzien van efficiëntere looplijsten, bedoeld voor toezichthouders en handhavers van illegaal vakantieverhuur. Check out the project's [documentation](http://petercuret.github.io/fixxx-looplijsten/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

Creating a superuser:
```bash
docker-compose run --rm web python manage.py createsuperuser
```
A superuser can be used to access the Django backend