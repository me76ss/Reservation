Setup
-----
You need ``python3.6``, ``pip``, ``virtualenv``, ``mysql`` for running the project. 
After you have installed the mentioned tools, clone the project and navigate to its root.<br>


Create a virtualenv with python3 bin file naming ``venv``:
```bash
python3 -m venv venv
```

Use the created ``venv`` environment:
```bash
source ./venv/bin/activate
```

Now install project dependency by running this command:
```bash
pip install -r ./requirements.txt
```

**Note:** Each time you add a new package to project, update requirements file by running this command:
```bash
pip freeze > requirements.txt
```

We will work with environment variables for personal config such as DB config. 
You can define env variables how you want, but our suggestion is using [direnv](https://direnv.net/). <br>

Direnv Config
-----
First you need to declare ``RESERVATION_BASE_PATH`` environment variable which points to the project root. <br> 
After installing it for you system and hooked it into your shell, do as follow:
```bash
cp .env.example .env
direnv allow
```
And then do you own config for variables in ``.env``


Database Initiation
-----
After creating a database file and db config in ``.env``, run following commands:
```bash
python manage.py migrate
python manage.py createsuperuser
```
