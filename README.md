# Course Registration (David Hackett)

## Setup

You must have docker [installed](https://www.docker.com/). Both the databases and the app are run using containers.

In main directory (course_registration) run:
`docker compose build --no-cache`

Then to run the project:
`docker compose up`

Before viewing the web app or running tests you need to setup the database.

## Testing

You'll need to run the test commands etc in the app container using the interactive shell.

To do this open a new command window (or tab) and run:
`docker exec -it course-registration-app-dh sh`

Then in the interactive shell first setup the database by running:
`python setup_db.py`

Then run the tests using pytest:
`pytest`

If you make updates using the app or you want to rerun the tests run the setup_db script again. In other words always run setup_db.py before testing.

To exit the interactive shell run:
`exit`

## Viewing the app

Ensure you've setup the db at least once using the instructions from testing.

Navigate to [http://localhost:5000/](http://localhost:5000/)

## Cleanup

Ctrl-c in the command window running the docker containers you can then run:
`docker compose down -v`

## Requirements Met

- A Student can view their current courses
- A Student can register for a class
- A Student can drop a class
- A Student can search for a course by id
- Has MySql Database for everything but notifications
- Has NoSql (Mongo) database for notification

## Requirements to meet still

- A student can request instructor consent
- A student can request department chair consent to overload schedule
- A student can view restrictions
- A student is shown other sections if a class is not available
