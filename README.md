#### ASSIGNMENT 1



### You must install Python3 and Pip3 to run this project

> I suggest using Python 3.10.3 and Pip 22.0.4



### DATABASE: PostgreSQL

> username: admin

> password: admin

> database_name: Exe1

### CREATE VIRTUAL ENVIRONMENT

> python3 -m venv env

> source env/bin/activate

### DEACTIVE VIRTUAL ENVIRONTMENT

> source env/bin/deactive

### INSTALL LIBRARY

> pip install -r requirements.txt

### Make sure to run the initial migration commands to update the database.

> flask db init

> flask db migrate --message 'initial database migration'

> flask db upgrade



### To run the project:

> flask run



### Note: you need to create a user first

> You can view all APIs on http://127.0.0.1:5000

> To use other API, you need to run the login API first to get Authorization Token