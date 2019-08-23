A cookiecutter template for an API only Django Project.

# Core functionality

This template is meant to be used for projects hosted on AWS. It is split into Local and Production configs.
Local config uses a local PostgreSQL 10.6 database. Production config is targeted at AWS RDS solution. It also uses S3 buckets for file storage.

Requests can be handled either using Django Rest Framework or GraphQL. Authentication is handled through DRF Authentication library (django-allauth & django-rest-auth). By default GraphQL view is protected, and accessible only by logged in users.

Project is run through docker. For local developement use docker-compose.yml . For production deployment, it uses Travis, nginx and certbot for https.
