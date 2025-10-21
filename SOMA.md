# IKR Plantations Project - Complete Setup Guide

## Step 1: Create Virtual Environment and Install Dependencies

```bash
# Create project directory
mkdir ikr_project
cd ikr_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Create requirements.txt first (see below)
# Then install dependencies
pip install -r requirements.txt
```

## Step 2: Project Structure Creation

After activating your virtual environment, create all directories:

```bash
# Create main project structure
mkdir -p ikr_project/settings
mkdir -p apps/users apps/agents apps/listings apps/inquiries apps/pages
mkdir -p static/css static/js static/images static/scss
mkdir -p templates/partials templates/users templates/agents templates/listings/partials
mkdir media
```

## Step 3: Initialize Django Project

```bash
# Start Django project (this creates manage.py and initial files)
django-admin startproject ikr_project .

# Create apps
python manage.py startapp users apps/users
python manage.py startapp agents apps/agents
python manage.py startapp listings apps/listings
python manage.py startapp inquiries apps/inquiries
python manage.py startapp pages apps/pages
```
#link to isaacrono.onrender.com
## Step 4: Apply All Configuration Files

Copy all the files provided in the artifacts below into your project structure.

## Step 5: Run Migrations

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## Step 6: Create Superuser

```bash
python manage.py createsuperuser
# Follow prompts to set username, email, and password
```

## Step 7: Collect Static Files (for production)

```bash
python manage.py collectstatic --noinput
```

## Step 8: Run Development Server

```bash
# Run on default port 8000
python manage.py runserver

# Or specify a port
python manage.py runserver 8080
```

## Step 9: Access the Application

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Listings**: http://127.0.0.1:8000/listings/
- **Agents**: http://127.0.0.1:8000/agents/

## Docker Setup (Optional)

```bash
# Build and run with Docker
docker-compose up --build

# Run migrations in Docker
docker-compose exec web python manage.py migrate

# Create superuser in Docker
docker-compose exec web python manage.py createsuperuser
```

## Environment Variables

Create a `.env` file in the root directory with the following:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## Project Features

1. **Custom User Model** with email authentication
2. **Agent Profiles** linked to users
3. **Property Listings** with categories, locations, and amenities
4. **Inquiry System** for user-agent communication
5. **Search and Filter** functionality
6. **Responsive Design** with Bootstrap
7. **Admin Panel** fully configured
8. **Docker Support** for easy deployment

## Next Steps

1. Customize the CSS in `static/css/main.css`
2. Add your logo to `static/images/logo.png`
3. Configure email settings in production settings
4. Set up media file storage for production
5. Add more categories and locations through admin panel

## Troubleshooting

- If you see "no module named apps", ensure your PYTHONPATH includes the project root
- For static files not loading, run `python manage.py collectstatic`
- For permission errors on media uploads, check folder permissions
- Ensure your `.env` file is in the root directory and properly formatted