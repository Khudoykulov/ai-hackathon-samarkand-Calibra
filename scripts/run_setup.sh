#!/bin/bash

echo "Setting up AI Irrigation System..."

# Install requirements
echo "Installing Python packages..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "Creating superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Setup initial data
echo "Setting up initial data..."
python manage.py shell < scripts/setup_initial_data.py

# Generate sample data
echo "Generating sample data..."
python manage.py shell < scripts/generate_sample_data.py

echo "Setup completed!"
echo "You can now run the server with: python manage.py runserver"
echo "Admin panel: http://localhost:8000/admin (admin/admin123)"
echo "Dashboard: http://localhost:8000/"
