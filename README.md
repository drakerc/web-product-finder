# Regex finder
This project is used to store brands and their associated regexes so you can filter products based on the provided/saved regex.

Allows to create a new brand (or subbrand), add regex rules for it and test them against a pandas dataframe, export brand's rules to a CSV file and just test regex rules against the dataframe without saving them.

# Usage
After starting the project (refer to Starting the project), visit the Swagger documentation available at http://localhost/api/swagger (or replace localhost with the proper address) to find the available API endpoints

Here are some of the most important endpoints. Please consult the Swagger documentation to find out what each endpoints expects to receive and what it returns:

* http://localhost/api/v1/brand/ - you can create a new brand instance (POST) or it returns all created brands (GET)
* http://localhost/api/v1/brand/<brand_id> (e.g. http://localhost/api/v1/brand/1) - read the details of a brand, delete it, or edit
* http://localhost/api/v1/brand/<brand_id>/export-rules (e.g. http://localhost/api/v1/brand/1/export-rules) - export the regexes of a brand (to CSV) (POST)
* http://localhost/api/v1/brand/<brand_id>/regex (e.g. http://localhost/api/v1/brand/1/regex) - get the list of brand's regexes (GET) or create a new regex (POST)
* http://localhost/api/v1/brand/<brand_id>/regex/<regex_id> (e.g. http://localhost/api/v1/brand/1/regex/1) - read the details of a regex, delete it or edit (GET, DELETE or PUT)
* http://localhost/api/v1/brand/<brand_id>/regex/<regex_id>/search-regex (e.g. http://localhost/api/v1/brand/1/regex/1/search-regex) - find products that match the saved regex (GET)
* http://localhost/api/v1/search-regex (e.g. http://localhost/api/v1/search-regex) - find products that match the POSTed regex without saving it (POST)






# Implementation details
Created using Django REST Framework. Containerized using docker-compose.
Uses SQLite on dev environment and MySQL on production env.
Documentation (swagger) created using drf-yasg.

### Implementation notes
This project does not have any front-end (yet) as I assume that Swagger/DRF's panel should be enough to test it.
There are also no tests (yet) as I wasn't really sure about a few very important business-logic details (and don't want to waste time on it and then rewrite it).
This project is RESTful, however, it uses monolithic architecture instead of microservices. 
I believe that adding microservices here is not really worth it yet, as the codebase is too small and adding a REST/AMPQ
based communication could slow things down and create a lot of issues during the development and it'd make the testing hard.
However, I have separated the business logic into a few services (`data_exporter`, `data_storage` and `regex_searcher`).
In the future, if needed, it's pretty easy to separate these services into microservices communicating via REST.

### Implementation problems
* The `data_storage` service is a singleton that keeps the products data in memory.
 This will cause problems in the future (scaling it will cause a lot of memory usage). However, I wasn't sure if using a DB to store products was OK according to the business logic.
* I'm converting pandas DataFrame to a list of objects. I'm pretty sure that it slows things down and the regex search
 could be faster on a DataFrame. However, to keep it more clean and Pythonic, I decided to use normal data structures.
* I had several doubts when it comes to the business logic. First of all, it just uses standard regexes instead of the
 in/out rules. I also didn't know what kind of formats do I need to support when exporting reports.

### Starting the project
* Install docker and docker-compose (I recommend this tutorial: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)
* Copy the gzip data file to `static/data/UK_outlet_meal.parquet.gzip` (or use a different path, but remember to edit it in the `.env` file)
* Copy `.env.dist` to `.env` (`cp .env.dist .env`) (and modify the database/ports variables if necessary)
* Execute `docker-compose build`
* Execute `docker-compose up -d` (or `docker-compose -f docker-compose.prod.yml up -d` in deployment environment)
* Apply migrations by using `docker-compose exec finder_python python manage.py migrate` (on production, use `docker-compose -f docker-compose.prod.yml exec finder_python python manage.py migrate --settings=home.settings.prod`)
* If there's a problem with static files (Django's panel does build properly, especially on production), use `docker-compose -f docker-compose.prod.yml exec finder_python python manage.py collectstatic --noinput`
* The project should be available at http://localhost/api

### Testing
Coming soon if needed
