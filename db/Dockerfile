# Official PostgreSQL image with our schema + seed data baked in
FROM postgres:16-alpine
COPY init.sql /docker-entrypoint-initdb.d/init.sql
