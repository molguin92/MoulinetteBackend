#Moulinette backend service.

##Deployment instructions:
###Required software:
1. Python 3.5+
2. Virtualenv
3. PostgreSQL/MySQL
4. (Optional) Autoenv

###Preparing the environment:
1. Create a virtual python environment in the root folder and activate it:
```bash
# virtualenv --python=3.5 ./venv
# . venv/bin/activate
```
2. Install Python libraries:
```bash
(virtualenv) pip install -r requirements.txt
```
3. Create a new database:
```bash
# createdb MOULINETTE
```
4. Set the appropiate environment variables (DATABASE_URL must, obviously, 
point to the previously created database):
```bash
export DATABASE_URL='postgresql://localhost/MOULINETTE'
export SECRET_KEY='ultrasecretmegakey'
```
This is done automatically if using Autoenv.
5. Create the database scheme:
```bash
(virtualenv) python migrate.py db init
(virtualenv) python migrate.py db migrate
(virtualenv) python migrate.py db upgrade
```
Also, after every change to the database model, run the last two commands 
again.

### Running the application:
1. Locally, for testing purposes:
```bash
(virtualenv) python moulinette_run.py
```
2. Using gunicorn, a (very) lightweight HTTP server:
```bash
(virtualenv) gunicorn moulinette:app
```

