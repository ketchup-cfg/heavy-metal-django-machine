
# Heavy Metal Machine: A Music Forum

This is a full-stack Python web application built with the Django framework to support the world's least favorite music forum.


## Installing Dependencies

In order to run this application, you will need to install the PyPi packages referenced in the [requirements.txt](https://github.com/ketchup-cfg/learning-flask/blob/main/requirements.txt) file (uh, and also make sure to have Python setup and configured):

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Configuring the Secret Key

In order for the application to run, a secret key will need to be generated and then set to an environment variable named `SECRET_KEY`.

To generate the secret key, the following utility method provided by Django can be used:
```python
from django.core.management.utils import get_random_secret_key  
get_random_secret_key()
```

After this, the `SECRET_KEY` environment variable will need to be set to the generated secret key value from the previous step:
```bash
$ echo SECRET_KEY=totallyrealsecretkey1
```

## Initializing the Database

To ensure that the application actually works, you will also need to initialize the application database.

Thankfully, the application is configured to use SQLite out of the box, so the database can be configured by just applying migrations:

```bash
$ python manage.py migrate
````

## Running the App

In order to run the application, enter the following command into your terminal:

```bash
$ python manage.py runserver
```

## Check Test Coverage

To check total test coverage for the application, run the following to gather test data:

```bash
$ coverage run --source='.' manage.py test
```

then run the following to generate the coverage report:

```bash
$ coverage report
```

If you would like to view a more detailed coverage report, run the following:

```bash
$ coverage html
```

then open htmlcov/index.html in a web browser.

