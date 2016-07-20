# Google app engine blog/cms

A multi user blog with user accounts, implemented on Google App Engine.

## Features

* Uses webapp2 framework for backend, Bootstrap 3 for frontend
* Templating system with Jinja2
* Google datastore to persist user accounts and posts
* Client and server side authentication

## Installation

First make sure you have a version of Python 2.7, as well as the latest google app engine python toolkit installed and available on your machines $PATH.

`git clone` and navigate to main directory

`dev_appserver.py .` to start develeopment server

To deploy the app, as per the Google App Engine documentation: `appcfg.py -A [YOUR_PROJECT_ID] -V v1 update ./`
Your project will be running live at `http://[YOUR_PROJECT_ID].appspot.com/`.

## TODO

* Add an admin dashboard and account
* Add a user profile page with relevant user information and dashboard
* Connect extra form options on new post page - image, tags, status - to post model
* Add sorting blog posts by dates and categories
* Write unit and functional tests
* Update styling
