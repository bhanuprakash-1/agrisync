# AgriSync ![Status active](https://img.shields.io/badge/Status-active%20development-2eb3c1.svg) ![Django 2.1.5](https://img.shields.io/badge/Django-2.1.5-green.svg) ![Python 3.6](https://img.shields.io/badge/Python-3.6-blue.svg) [ ![Build Status](https://api.travis-ci.com/hirenchalodiya1/agrisync.svg?branch=master)](https://github.com/hirenchalodiya1/agrisync/)

### Purpose

A web application to guide farmers through different agriculture practices.
This project includes:
- A main `web portal` which can be updated dynamically through an admin interface.
- A `forum/discussion` app for general purpose discussions.
- An app called `Konnekt` to find/search people with a certain required skill set.

### Installation:
Requirements:
- Python 3 runtime
- Pip
- Django 2.1.5
- Other dependencies in `Pipfile`

Procedure:

- Install [python](https://www.python.org/downloads/) in your environment(pre-installed on Ubuntu).
- Navigate to the cloned repository.
    ```
    cd <project_directory_name>     # agrisync
    ```
- Install dependencies
    ```
    pip3 install pipenv
    pipenv install --dev
    ```
- Create a new virtual environment and activate it.
    ```
    source "$(pipenv --venv)"/bin/activate
    ```
- Copy `.env.example` to `.env`
    ```
    cp .env.example .env
    ```
- Change to `src` directory
    ```
    cd src
    ```
- Make database migrations
    ```
    python manage.py makemigrations 
    python manage.py migrate 
    ```
- Create a superuser
    ```
    python manage.py createsuperuser 
    ```
- Run development server on localhost
    ```
    python manage.py runserver 
    ```
