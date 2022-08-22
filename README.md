# Vite Une Recette [![Build Status](https://travis-ci.com/slesouef/Whats-for-diner.svg?branch=develop)](https://travis-ci.com/slesouef/Whats-for-diner)

## Project Description
Create a website that will allow users to find recipes by searching for one or
more ingredients. The primary goal is to limit waste by enabling user to use
the ingredients they have on hand instead of throwing them away.
User can also add their own recipes to the site and share them.

## Requirements
This project supports Python 3.9 and is build using the Django framework
Please install the other requirements by running  
`pipenv install`

In order to install the development environment requirements, run  
`pipenv install --dev`


## Virtual Environment Configuration
The project virtual environment in managed at installation by pipenv.
Switch to the project's virtual environment via  
`pipenv shell`

## Database Configuration
This project is configured to use a PostgreSQL 13 database.

The test database uses the following configuration:   
``` 
Name: wfd_dev 
User: wfd_dev
Password: wfd_dev
Host: localhost
Port: 5432
```

## Usage
A live version of this website currently resides at:   
[viteunerecette.xyz](https://viteunerecette.xyz)

A local version of the site can be run using   
`python manage.py runserver`

## Tests
The projects test suite can be run via  
`python manage.py test`

The project uses [Travis-CI](https://www.travis-ci.com/) for continuous
integration and deployment.  
The project pipeline is [here](https://app.travis-ci.com/github/slesouef/Whats-for-diner)
