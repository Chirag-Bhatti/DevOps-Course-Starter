# **DevOps Apprenticeship: Project Exercise**

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

&nbsp;
## **System Requirements**

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

&nbsp;
## **Dependencies**

### **Virtual Environment**

The project uses a virtual environment to isolate package dependencies. 

To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```
&nbsp;
### **Setting up the .env files**

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

&nbsp;
### **Trello**

The project uses the Trello API. You will need to sign up for an account [here](https://trello.com/signup) first 

After this, generate an API key and token, see instructions [here](https://trello.com/app-key)

Once you have these, save the API key and token generated on the `.env` file against the `API_KEY` and `TOKEN` variables

It would also be useful to attain the ID of the board you wish the program to use, and save this against the `BOARD_ID` variable

You can attain this by running a GET request to https://api.trello.com/1/members/me/boards (using something like Postman), with the query parameters `key` and `token` set to those generated above to get your board(s), and copy the id of the one you want to use from the response

&nbsp;
## **Running the App**

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.
