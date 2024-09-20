Fatmug videoProcessing Assignment


For building and running container use - "docker-compose up --build" & for creating required databaseschema use "docker-compose run web python manage.py migrate"  in a differnt terminal.

Note : Genrally the migrations part is included in the Dockerfile running itself but as Postgresql is an Asynchronous service we need to perform mogrations separately.
