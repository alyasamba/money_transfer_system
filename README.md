The Money Transfer System is REST API service based on Django Rest Framework and Docker containers.
The purpose of the project is a providing service for money transfering from user to user in different currencies and exchange rates. 
The system allows operating with plenty of currencies and chronological exchange rates of currency courses.
It automatically downloads a list of currencies and their exchange rates from service https://api.exchangeratesapi.io/latest
Supports JSON Web Token authorization.

Functionality of the system is described by its REST API endpoints.

Main endpoints:
 - /api/token/ - authenticate through JSON Web Tokens;
 - /api/token/refresh/ - refresh JWT-token;
 - /api/users/ - user issues;
 - /api/money/ - money transfer issues
 
USERS endpoints:
 - /api/users/ - get list of all users (HTTP GET method);
 - /api/users/create/ - register new user (HTTP POST method);
 - /api/users/accounts/ - get current user's accounts including balance information (HTTP GET method);
 - /api/users/accounts/create/ - create new account for current user (HTTP POST method);
 - /api/users/{id}/ - get info about user of particular id (HTTP GET method);
 - /api/users/{id}/edit/ - edit particular user (HTTP PATCH method);
 - /api/users/{id}/accounts/ - get accounts of particular user (HTTP GET method).
 
MONEY endpoints:
 - /api/money/currencies/ - get list of currencies (HTTP GET method);
 - /api/money/courses/ - get list of courses rates (HTTP GET method);
 - /api/money/transfers/ - get list transfers of current user (HTTP GET method);
 - /api/money/transfers/create/ - create new transfer (HTTP POST method).
 
Project directory structure:
 - postgres - directory for building PostgreSQL container;
 - nginx - directory for building Nginx container;
 - redis - directory for building Redis container for supporting ampq based on redis for Celery asynchronous tasks;
 - web - directory for building WSGI container for supporting gunicorn wsgi server, contains Django source files of the system;
 - docker-compose.yml - Docker Compose CE YAML file;
 - money_transfer_system.service - SystemD service configuration file;
 - setup.sh - Bash script file for installing service;
 - Technical task.txt - text file containing functional and nonfunctional requirements of the project.
 
 Each docker directory of the system (postgres, redis, nginx, web) contains inside 'log' subdirectory for logging subsystem events and errors. 

Django project is located in ./web/src/project. 
The project is provided by testing module located in ./web/src/project/money/tests.py.
Python requirements-file path is ./web/requirements.txt. 
Asynchronous Celery task periodically fetches currency/rates json-data and upload currencies and exchange rates in database. It is coded in ./web/src/project/money/tasks.py.

After the first start of the service, you need to create a superuser:
 1. docker exec -it mts_wsgi /bin/bash
 2. python manage.py createsuperuser
 3. edit docker-compose.yml - add to web service such records:
   environment:
    - ADMIN_EMAIL=email
    - ADMIN_PASSWORD=password
    
   (email, password from step 2)
    
web service must be like that:

    build: ./web/
    image: wsgi:money_transfer_system
    hostname: mts_wsgi
    container_name: mts_wsgi
    network_mode: host
    environment:
     - ADMIN_EMAIL=email
     - ADMIN_PASSWORD=password
    depends_on:
      - postgres
      - redis
    volumes:
      - ./web/celery/log:/tmp/celery.log
      - ./web/log:/var/log/gunicorn
      - ./web/src/project:/var/www/money_transfer_system
      - ./web/init/gunicorn.py:/etc/gunicorn/gunicorn.py
