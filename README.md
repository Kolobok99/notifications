Notifications Service
---
Техническое задание
---
<a href='https://www.craft.do/s/n6OVYFVUpq0o6L'>ссылка на тз</a>

Описание
---
Notifications Service - REST API для рассылки сообщений клиентам

Функционал
---
- добавления/обновление/удаление данных клиентов
- добавления новой рассылки со всеми её атрибутами
- получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
- получения детальной статистики отправленных сообщений по конкретной рассылке
- обновления атрибутов рассылки
- удаления рассылки
- обработки активных рассылок и отправки сообщений клиентам

Дополнительные задания:
---
- 1. организовать тестирование написанного кода
- 2. обеспечить автоматическую сборку/тестирование с помощью GitLab CI
- 3. подготовить docker-compose для запуска всех сервисов проекта одной командой
- 5. сделать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного API.
- 6. реализовать администраторский Web UI для управления рассылками и получения статистики по отправленным сообщениям
- 8. реализовать дополнительный сервис, который раз в сутки отправляет статистику по обработанным рассылкам на email
- 9. удаленный сервис может быть недоступен, долго отвечать на запросы или выдавать некорректные ответы. Необходимо организовать обработку ошибок и откладывание запросов при неуспехе для последующей повторной отправки. Задержки в работе внешнего сервиса никак не должны оказывать влияние на работу сервиса рассылок.
- 11. реализовать дополнительную бизнес-логику: добавить в сущность "рассылка" поле "временной интервал", в котором можно задать промежуток времени, в котором клиентам можно отправлять сообщения с учётом их локального времени. Не отправлять клиенту сообщение, если его локальное время не входит в указанный интервал.
- 12. обеспечить подробное логирование на всех этапах обработки запросов.

Системные требования
---
- Windows / Linux / MacOS
- Docker
- Docker-compose

Стек 
---
- Python
- Django
- PostgreSQL
- Nginx
- gunicorn
- Docker, docker-compose
- Redis

Зависимости
---
- Django==4.1.2
- djangorestframework==3.14.0  
- celery==5.2.7  
- redis==4.3.4  
- psycopg2==2.8.5  
- gunicorn==20.1.0  
- requests==2.28.1  
- arrow==1.2.1
- django-filter==22.1
- pytest==7.1.3
- pytest-django==4.5.2
- loguru==0.6.0


Запуск проекта
---
1.  Клонировать проект и перейти в его корень:

		git clone https://gitlab.com/izolotavin99/notifications
		cd notifications

2. Создать директорию с .env.prod. файлами

		mkdir .env_files.prod
		cd .env_files.prod
3. Инициализировать .env.prod.settings со следующими переменными:

	    DEBUG=0
		SECRET_KEY={your_secret_key}
		DJANGO_ALLOWED_HOSTS={your_host_ip}
		TIME_ZONE={your_time_zone_name}		

		SQL_ENGINE=django.db.backends.postgresql
	    SQL_NAME={your_sql_name}
        SQL_USER={your_sql_user}
        SQL_PASSWORD={your_sql_password}
        SQL_HOST=db
        SQL_PORT={your_sql_port}

		REDIS_HOST=redis
		REDIS_PORT=6379
		
		echo API_KEY={your_api_key}

4. Инициализировать .env.prod.email со следующими переменными:

		EMAIL_HOST={your_email_host}
		EMAIL_PORT={your_email_port}
		EMAIL_HOST_PASSWORD={your_email_password}
		ADMIN_EMAIL={your_admin_email}

5. Инициализировать .env.prod.celery со следующими переменными:
		
     	DB_HOST=db
		DB_NAME={your_sql_name}
		DB_USER={your_sql_user}
		DB_PASS={your_sql_password}

6. Инициализировать .env.prod.db со следующими переменными:

		POSTGRES_DB={your_sql_name}
		POSTGRES_USER={your_sql_user}
		POSTGRES_PORT={your_sql_port}
		POSTGRES_PASSWORD={your_sql_password}

3. Собрать проект

		cd ../docker-composes
		docker compose -f docker-compose.ci.yml build
4. Запустить проект

		docker compose -f docker-compose.ci.yml up

6. Создать супер-пользователя

		docker compose -f docker-compose.ci.yml exec web bash
		python manage.py createsuperuser

Запуск тестов:
---

	    docker compose -f docker-compose.ci.yml run --rm web pytest

Документация API:
---
полная документация доступна по адресу: 	
		http://{your_ip}/api/v1/docs/

    - GET  api/v1/client/ - получить список всех клиентов
    - POST api/v1/client/ - добавить нового клиента
    - GET  api/v1/client/{phone}/ получить клиента по его phone
    - PATCH api/v1/client/{phone}/ изменить данные клиента по его phone
    - DELETE api/v1/client/{phone}/ удалить клиента по его phone

	- GET  api/v1/tag/ - получить все тэги
	- POST api/v1/tag/ - добавить новый тэг
	- GET  api/v1/tag/{tag}/ получить тэг по его tag
	- DELETE api/v1/tag/{tag}/ удалить тэг по его tag

	- GET  api/v1/mailing/ - получить все рассылки со статистикой
	- POST api/v1/mailing/ - добавить новую рассылку
	- GET  api/v1/mailing/{id}/ получить рассылку по еe id со статистикой 
	- PATCH api/v1/mailing/{id}/ изменить данные рассылки по ее id
	- DELETE api/v1/mailing/{id}/ удалить рассылку по ее id

	- GET api/v1/statistic/ - получить все статистики рассылок


		