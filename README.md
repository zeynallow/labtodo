## Lab ToDo

Include:

 - Python
 - Django
 - Django Channels
 - Celery worker + Celery beat
 - PostgreSQL
 - Redis

### Docker

1. Start Docker Native
2. Build images - `docker-compose build`
3. Create the database migrations - `docker-compose run web python manage.py migrate`
4. Start services - `docker-compose up`
5. View in browser http://127.0.0.1:8000/
