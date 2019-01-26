## New Django Project Setup

### Set git repository first

```git clone <repo link>```

or

```git remote add origin <repo link>```

```git push --set-upstream origin master```

```git brach --set-upstream-to=origin/master master```

### Add .gitignore files

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
*.sqlite3
.idea/

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# dotenv
.env

# virtualenv
.venv
venv/
ENV/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.DS_Store

# Django migrations
migrations/

# Project asset folders
staticfiles/
static/
media/

# Database
db.sqlite3

# VueJS files
.DS_Store
node_modules/
/dist/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
/test/unit/coverage
/test/e2e/reports
selenium-debug.log

# Editor directories and files
.idea
*.suo
*.ntvs*
*.njsproj
*.sln
```

### Pipenv setup

```pip3 install pipenv```

```source "$(pipenv --<venv_name>)"/bin/activate```

### Add environment variable

Write all environment variable in .env.example file run following command

```cp .env.example .env```

and make required changes in .env file


### Add CI integration

Here I have used Travis for my project

.travis.yml
```
language: python
python:
  - "3.6"
addons:
  postgresql: "9.6"
dist: trusty
before_install:
  - export DJANGO_SETTINGS_MODULE=gymkhana.settings
  - export DJANGO_SECRET_KEY='q$o5mx19x9(9_^rzqf@o@s^t%t!ghix7($f9ymy49_^ryzq9x9'
  - psql -c "CREATE DATABASE <dbname>;" -U postgres
  - psql -c "CREATE USER <dbuser> WITH LOGIN PASSWORD '<dbpass>';" -U postgres
  - psql -c "ALTER ROLE <dbuser> WITH CREATEDB;" -U postgres
  - psql -c "GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <dbuser>;" -U postgres
install:
  - pip3 install coveralls
  - pip3 install pipenv
  - pipenv install --dev
script:
  - cp .env.example .env
  - cd src
  - source "$(pipenv --venv)"/bin/activate
  - flake8 .
  - python3 manage.py makemigrations
  - python3 manage.py migrate
  - coverage run manage.py test
#after_success:
#  - coveralls

```

### Add flake8

```pipenv install flake8```
In .flake8 file
```
[flake8]
max-line-length = 120
exclude = gymkhana/settings/*, manage.py, migrations
```

### Setup REAME.md for your project
