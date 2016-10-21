# Digital Ocean Setup

## Prerequisites
* Create a droplet on DigitalOcean and buy a domain name.
* Change the nameservers for your domain to `ns1.digitalocean.com`, `ns2.digitalocean.com` & `ns3.digitalocean.com`.
* Add your domain name to the domain list.
* Create a new DNS record for your domain:

```
Type  = 'A'
Host  = 'www'
Value = IP Address of Server
```

* Connect to the server via SSH or the console provided by DigitalOcean.

## Setup Instructions
### STEP 1: Update All Existing Packages
```
sudo apt-get update
sudo apt-get upgrade
```

### STEP 2: Setup a Virtual Environment
```
sudo apt-get install python-virtualenv
sudo virtualenv /opt/myenv
```

### STEP 3: Install Django
* Ensure that the virtual environment is currently active:

```
source /opt/myenv/bin/activate
```

* Now use pip to install Django:

```
pip install django
```

### STEP 4: Install PostgreSQL
* Deactivate the virtual environment:

```
deactivate
```

* Install the necessary packages:

```
sudo apt-get install libpq-dev python-dev
sudo apt-get install postgresql postgresql-contrib
```

### STEP 5: Install NGINX
```
sudo apt-get install nginx
```

### STEP 6: Install Gunicorn
* Reactivate the virtual environment and install Gunicorn:

```
source /opt/myenv/bin/activate
pip install gunicorn
```

### STEP 7: Setup PostgreSQL
* First run the command:

```
sudo su - postgres
```

* This should prompt a change in user to postgres. So your terminal will now read `postgres@servername`.

* Create the database - `TripBuddySG`:

```
createdb TripBuddySG
```

* Launch the postgres command line:

```
psql
```

* Change the password for postgres:

```
ALTER USER "postgres" WITH PASSWORD "<PASSWORD>";
GRANT ALL PRIVILEGES ON DATABASE "TripBuddySG" TO "postgres";
```

### STEP 8: Setup the Django Project
```
cd /opt/myenv
source /opt/myenv/bin/activate
sudo apt-get install git
git clone https://github.com/TripBuddySG/TripBuddySG
pip install psycopg2
pip install celery
pip install python-social-auth
pip install stripe
pip install Pillow
sudo apt-get install libjpeg-dev libpng12-dev
sudo apt-get install zlib1g-dev
sudo apt-get install libtiff5
sudp apt-get install libfreetype6
sudo apt-get install liblcms liblcms-dev liblcms-utils libwebp-dev libopenjpeg-dev
```

* At this point, create a Facebook and Django app to get your secret keys and edit the `TripBuddySG/keys.py` file to fill in all the keys.

* Now, create a super user:

```
python manage.py createsuperuser
```

* When prompted, enter the username `TripBuddySG` and a password.

* Finally, run the following command to collect static files:

```
python manage.py collectstatic
```

### STEP 9: Configure Gunicorn
* At this point, if you run the following command, you should see a website without static files loaded at `<domainname>:8001`:

```
gunicorn TripBuddySG.wsgi:application --workers=3 --bind <domainname>:8001
```

* A small bash script can be used to execute the command above. Open a new file in nano:

```
nano /bin/gunicorn_TripBuddySG.bash
```

* Enter the following into the bash script:

```bash
#!/bin/bash
NAME="TripBuddySG"                             # name of the application
DJANGODIR=/opt/myenv/TripBuddySG               # Django project directory
GROUP=webapps                                  # the group to run as
NUM_WORKERS=3                                  # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=TripBuddySG.settings    # which settings file should Django use
DJANGO_WSGI_MODULE=TripBuddySG.wsgi            # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment

cd $DJANGODIR

source ../bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)

exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \ 
--log-level=debug \
--log-file=-
```

* Save the file and exit nano. Next, make the script executable using:

```
sudo chmod u+x bin/gunicorn_TripBuddySG.bash
```

* Now the server can be started by running:

```
/bin/gunicorn_TripBuddySG.bash
```

## STEP 10: Configure NGINX
* If you had previously launched the server, kill the process by using ctrl-c or cmd-c.

* First start the NGINX service by calling:

```
sudo service nginx start
```

* Open a new file `TripBuddySG.nginxconf` in nano:

```
nano /etc/nginx/sites-available/TripBuddySG/TripBuddySG.nginxconf
```

* Insert the following in the file:

```
upstream TripBuddySG_server {
  server tripbuddy.sg:8001 fail_timeout=0;
}

server {
  listen 80;
  server_name <domainname>;
  client_max_body_size 4G;

  access_log /opt/myenv/logs/nginx-access.log;
  error_log /opt/myenv/logs/nginx-error.log;

  location /static/ {
    alias /opt/myenv/staticfiles/;
  }

  location /media/ {
    alias /opt/myenv/TripBuddySG/media/;
  }



  location / {
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;


    # enable this if and only if you use HTTPS, this helps Rack
    # set the proper protocol for doing redirects:
    # proxy_set_header X-Forwarded-Proto https;


    # pass the Host: header from the client right along so redirects
    # can be set properly within the Rack application
    proxy_set_header Host $http_host;


    # we don't want nginx trying to do something clever with
    # redirects, we set the Host: header above already.
    proxy_redirect off;


    # set "proxy_buffering off" *only* for Rainbows! when doing
    # Comet/long-poll stuff.  It's also safe to set if you're
    # using only serving fast clients with Unicorn + nginx.
    # Otherwise you _want_ nginx to buffer responses to slow
    # clients, really.

    # proxy_buffering off;


    # Try to serve static files from nginx, no point in making an
    # *application* server like Unicorn/Rainbows! serve static files.
    if (!-f $request_filename) {
      proxy_pass http://TripBuddySG_server;
      break;
    }
  }
}
```

* Save and exit.

* Create a symbolic link to the sites-enabled folder:

```
sudo ln -s /etc/nginx/sites-available/TripBuddySG/TripBuddySG.nginxconf /etc/nginx/sites-enabled/TripBuddySG
```

* Restart nginx:

```
sudo service nginx restart
```

## STEP 11: Launch
```
/bin/gunicorn_TripBuddySG.bash
```

* When exiting from terminal, do not press ctrl-c or cmd-c. This will ensure that the server runs in the background.
