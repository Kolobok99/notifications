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
- 5. сделать так, чтобы по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного API. Пример: [https://petstore.swagger.io](https://petstore.swagger.io)
- 6. реализовать администраторский Web UI для управления рассылками и получения статистики по отправленным сообщениям
- 8. реализовать дополнительный сервис, который раз в сутки отправляет статистику по обработанным рассылкам на email
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
- Celery
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

2. Инициализировать .env.prod. файлы

		mkdir .env_files.prod
		cd .env_files.prod
	    
	    echo DEBUG=0 >> .env.prod.settings
		echo SECRET_KEY=your_secret_key >> .env.prod.settings
		echo DJANGO_ALLOWED_HOSTS=your_host_ip >> .env.prod.settings
		echo TIME_ZONE=your_time_zone_name >> .env.prod.settings		

		echo SQL_ENGINE=django.db.backends.postgresql >> .env.prod.settings
	    echo SQL_NAME=your_sql_name >> .env.prod.settings
        echo SQL_USER=your_sql_user >> .env.prod.settings
        echo SQL_PASSWORD=your_sql_password >> .env.prod.settings
        echo SQL_HOST=db >> .env.prod.settings
        echo SQL_PORT=your_sql_port >> .env.prod.settings

		echo REDIS_HOST=redis >> .env.prod.settings
		echo REDIS_PORT=6379 >> .env.prod.settings

		echo EMAIL_HOST=your_email_host >> .env.prod.email
		echo EMAIL_PORT=your_email_port >> .env.prod.email
		echo EMAIL_HOST_PASSWORD=your_email_password >> .env.prod.email
		echo ADMIN_EMAIL=your_admin_email >> .env.prod.email
		
		echo API_KEY=your_api_key >> .env.prod.settings

		echo DB_HOST=db >> .env.prod.celery
		echo DB_NAME=your_sql_name >> .env.prod.celery
		echo DB_USER=your_sql_user >> .env.prod.celery
		echo DB_PASS=your_sql_password >> .env.prod.celery

		echo POSTGRES_DB=your_sql_name >> .env.prod.db
		echo POSTGRES_USER=your_sql_user >> .env.prod.db
		echo POSTGRES_PORT=your_sql_port >> .env.prod.db
		echo POSTGRES_PASSWORD=your_sql_password >> .env.prod.db

3. Собрать проект

		cd ../docker-composes
		docker compose -f docker-compose.ci.yml build
4. Запустить проект

		docker compose -f docker-compose.ci.yml up
5. Создать супер-пользователя

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
    - GET  api/v1/client/{int:pk}/ получить клиента по его id
    - PATCH api/v1/client/{int:pk}/ изменить данные клиента по его id
    - DELETE api/v1/client/{int:pk}/ удалить клиента по его id

	- GET  api/v1/tag/ - получить все тэги
	- POST api/v1/tag/ - добавить новый тэг
	- GET  api/v1/tag/{char:tag}/ получить тэг по его tag
	- DELETE api/v1/tag/{char:tag}/ удалить тэг по его tag

	- GET  api/v1/mailing/ - получить все рассылки со статистикой
	- POST api/v1/mailing/ - добавить новую рассылку
	- GET  api/v1/mailing/{int:pk}/ получить рассылку по еe id со статистикой 
	- PATCH api/v1/mailing/{int:pk}/ изменить данные рассылки по ее id
	- DELETE api/v1/mailing/{int:pk}/ удалить рассылку по ее id

	- GET api/v1/statistic/ - получить все статистики рассылок


		