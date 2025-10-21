# IKR Plantations Project - Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Render.com (Recommended for Quick Deployment)

1. **Create a Render.com account** at https://render.com
2. **Connect your GitHub repository**
3. **Create a new Web Service**:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn ikr_project.wsgi:application --bind 0.0.0.0:$PORT`
4. **Add Environment Variables**:
   ```
   DJANGO_SETTINGS_MODULE=ikr_project.settings.production
   SECRET_KEY=your-generated-secret-key
   DEBUG=False
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ALLOWED_HOSTS=your-app-name.onrender.com
   ```
5. **Create a PostgreSQL database** in Render and link it
6. **Deploy!**

### Option 2: Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build -d

# Run migrations in container
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Option 3: Heroku Deployment

1. **Install Heroku CLI**
2. **Login to Heroku**: `heroku login`
3. **Create app**: `heroku create your-app-name`
4. **Add PostgreSQL**: `heroku addons:create heroku-postgresql:hobby-dev`
5. **Set environment variables**:
   ```bash
   heroku config:set DJANGO_SETTINGS_MODULE=ikr_project.settings.production
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   ```
6. **Deploy**: `git push heroku main`

## 📋 Pre-Deployment Checklist

- [ ] Static files collected (`python manage.py collectstatic`)
- [ ] Database migrations applied (`python manage.py migrate`)
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Environment variables configured
- [ ] ALLOWED_HOSTS updated for production domain
- [ ] DEBUG=False in production
- [ ] SECRET_KEY is strong and unique
- [ ] Database configured (PostgreSQL recommended)

## 🔧 Environment Variables Required

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
# Edit .env with your values
```

## 🌐 Domain Configuration

After deployment, update these settings:

1. **ALLOWED_HOSTS** in production settings
2. **CSRF_TRUSTED_ORIGINS** if using CSRF protection
3. **CORS_ALLOWED_ORIGINS** if using CORS

## 📊 Database Setup

For production, use PostgreSQL:

```bash
# Install psycopg2-binary (already in requirements.txt)
# Configure DATABASE_URL in environment variables
```

## 📧 Email Configuration

Configure email settings for user notifications:

```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🔒 Security Checklist

- [ ] DEBUG = False
- [ ] SECRET_KEY is secure
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled
- [ ] CSRF protection enabled
- [ ] Secure cookies enabled
- [ ] Database credentials secure

## 🚀 Post-Deployment

1. **Test all functionality**
2. **Check admin panel access**
3. **Verify email sending**
4. **Test file uploads**
5. **Monitor logs**

## 🆘 Troubleshooting

- **Static files not loading**: Run `collectstatic` and check STATIC_URL
- **Database connection errors**: Verify DATABASE_URL format
- **500 errors**: Check logs and DEBUG settings
- **CSRF errors**: Add domain to CSRF_TRUSTED_ORIGINS

## 📞 Support

For deployment issues, check:
- Django deployment documentation
- Platform-specific guides (Render/Heroku/Docker)
- Project logs and error messages
