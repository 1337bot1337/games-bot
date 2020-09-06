Requirements & Set Up
=====================

Create a virtual environment for the project. You may use whatever tool: `pyenv`, the Python's `env` library or the `virtualenv` tool. Activate it then.

Install `pip-tools` to manage the project environment.
```bash
$ pip install pip-tools
```

We have a couple of commands to compile `requirements.txt` and update your virtual environment, to use them we have to install `invoke` tool.
```bash
$ pip install invoke
```

`inv <command>` should be executed from a directory where `invoke's` `tasks.py` file is allocated (the project root directory).

Compile `requirements.txt`:
```bash
$ inv pip.compile
```

Initially install or update the environment:
```bash
$ inv pip.sync
```

Or if you have not installed the `pip-tools`, you can install requirements
```bash
$ pip install -r requirements.txt
```

### Do the Database Migrations

If you will not override default environment variables, project will try to connect to DB called `core_db`.
To create the Postgres DB called `core_db` you need to:
```bash
$ createdb core_db
```

To initialize the database execute a command:

```bash
$ python manage.py migrate
```

# Run the Project

To run the project just execute a command:

```bash
$ python manage.py runserver 8000
```

The application will be available locally on a URL:

```
http://127.0.0.1:8000
```
