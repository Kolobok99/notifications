#! /bin/sh

mkdir  -p ./backend/.env_files.prod

echo DEBUG=0 >> ./backend/.env_files.prod/.env.prod.settings
#
echo SECRET_KEY=$PROD_SECRET_KEY >> ./backend/.env_files.prod/.env.prod.settings
echo DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1] >> ./backend/.env_files.prod/.env.prod.settings
#
echo SQL_ENGINE=$PROD_SQL_ENGINE >> ./backend/.env_files.prod/.env.prod.settings
echo SQL_NAME=$PROD_SQL_NAME >> ./backend/.env_files.prod/.env.prod.settings
echo SQL_USER=$PROD_SQL_USER >> ./backend/.env_files.prod/.env.prod.settings
echo SQL_PASSWORD=$PROD_SQL_PASSWORD >> ./backend/.env_files.prod/.env.prod.settings
echo SQL_HOST=$PROD_SQL_HOST >> ./backend/.env_files.prod/.env.prod.settings
echo SQL_PORT=$PROD_SQL_PORT >> ./backend/.env_files.prod/.env.prod.settings

echo DATABASE=$PROD_DATABASE >> ./backend/.env_files.prod/.env.prod.settings
#
echo MYSQL_DATABASE=$PROD_SQL_NAME >> ./backend/.env_files.prod/.env.prod.db
echo MYSQL_USER=$PROD_SQL_USER >> ./backend/.env_files.prod/.env.prod.db
echo MYSQL_PORT=$PROD_SQL_PORT >> ./backend/.env_files.prod/.env.prod.db
echo MYSQL_PASSWORD=$PROD_SQL_PASSWORD >> ./backend/.env_files.prod/.env.prod.db
echo MYSQL_ROOT_PASSWORD=$PROD_SQL_ROOT_PASSWORD >> ./backend/.env_files.prod/.env.prod.db


