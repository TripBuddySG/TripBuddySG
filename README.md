# TripBuddySG

This repository contains the code base for the website TripBuddySG. The project was built using the [Django framework](https://www.djangoproject.com/) and [PostgreSQL](https://www.postgresql.org/).

The front end repository can be found [here](https://github.com/TripBuddySG/TripBuddySG-FrontEnd).

# Setup Instructions

## Local Development
1. Clone the repository or download the [zip](https://github.com/TripBuddySG/TripBuddySG/archive/master.zip). 
2. Install all the required python dependencies using ```pip install -r dependencies.txt```.
3. Install [PostgreSQL](https://www.postgresql.org/), remember your password and set up a database called ```TripBuddySG```.
4. Create a superuser using ```python manage.py createsuperuser```. Enter username as ```TripBuddySG``` and password according to your choice. Remember these details.
5. Create all the required developer apps(Django App and Facebook) and change the keys at TripBuddySG/keys.py.
6. Change the email host at TripBuddySG/settings.py.
7. Run the server with ```python manage.py runserver```.
8. View the website at [http://localhost:8000](http://localhost:8000) or [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Deploy on Digital Ocean Server
Please refer [here](https://github.com/TripBuddySG/TripBuddySG/server-setup.md) for instructions to set up and deploy from a digital ocean server.

# Contributing
Please create an issue or submit a pull request if you wish to contribute. We love open source contributions. :smile: 

# Contributors
1. [Suyash Lakhotia](https://github.com/SuyashLakhotia)
2. [Nikhil Venkatesh](https://github.com/nikv96)
