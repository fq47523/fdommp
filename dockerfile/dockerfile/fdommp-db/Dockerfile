FROM mysql:5.7.27

# base
ENV MYSQL_ROOT_PASSWORD=fdommp


# sql

COPY fdommp-plugins/db/create_fdommp_database.sql /docker-entrypoint-initdb.d
