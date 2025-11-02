# 
# Build and start all services
docker-compose up -d --build

# Build without detach
docker-compose up --build

# View logs
docker-compose logs -f

docker-compose logs django-web

# Run migrations
docker-compose exec django-web python manage.py migrate

# Create superuser
docker-compose exec django-web python manage.py createsuperuser

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v


# To create a new app
python manage.py startapp core apps/core   
in apps include apps.core