if [ -e .env ]; then
    export $(cat .env | xargs)

    ## Start docker service
    sudo docker run -dp $DATABASE_PORT:3306 -v simple_message_app:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=$DATABASE_PWD -e MYSQL_USER=$DATABASE_USER -e MYSQL_PASSWORD=$DATABASE_PWD -e MYSQL_DATABASE=$DATABASE_NAME mysql:latest
else
    echo ".env file not found"
fi
