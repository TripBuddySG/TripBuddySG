# TripBuddySG

This repository contains the entire codebase for TripBuddySG. The back-end runs on [Django](https://www.djangoproject.com/) and [PostgreSQL](https://www.postgresql.org/) while the front-end is built using [Bootstrap](http://getbootstrap.com/) and [jQuery](https://jquery.com/) alongside vanilla HTML, CSS & JavaScript.

The front end repository can be found [here](https://github.com/TripBuddySG/TripBuddySG-FrontEnd).

# Setup Instructions

## Local Development
1. Clone this repository or download the [zip](https://github.com/TripBuddySG/TripBuddySG/archive/master.zip). 
2. Install all the required python dependencies using `pip install -r dependencies.txt`.
3. Setup [PostgreSQL](https://www.postgresql.org/) and create a database named `TripBuddySG`.
4. Create a superuser using `python manage.py createsuperuser`. Set the username - `TripBuddySG` - and a password.
5. Create the required developer apps (Django App & Facebook) and set the keys at `TripBuddySG/keys.py`.
6. Set the email host at `TripBuddySG/settings.py`.
7. Run the server with `python manage.py runserver`.
8. The website should now be running at [http://localhost:8000](http://localhost:8000).

## Deploy on Digital Ocean
Please refer [here](Server%20Setup.md) for instructions on setting up and deploying TripBuddySG on a Digital Ocean droplet.

# Contributing
Please create an issue or submit a pull request if you wish to contribute. We love open source contributions. :smile: 

# Contributors
1. [Suyash Lakhotia](https://github.com/SuyashLakhotia)
2. [Nikhil Venkatesh](https://github.com/nikv96)
