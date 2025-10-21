# 🚀 IKR Plantations - Render.com Deployment Guide

## Prerequisites
- GitHub account
- Render.com account (free tier available)

## Free Tier Information

Render offers free instances for web services, PostgreSQL databases, and Key Value instances. Free instances are perfect for testing, hobby projects, or previewing Render's platform but have important limitations.

### Free Web Services
- **Spinning down**: Services spin down after 15 minutes of inactivity, causing a delay (up to 1 minute) for the next request.
- **Monthly usage limits**: 750 free instance hours per workspace. Exceeded hours suspend services until the next month.
- **Bandwidth and pipeline**: Counts against monthly included allotments. Excess may require payment or suspend services.
- **Limitations**:
  - No scaling beyond a single instance
  - No persistent disks
  - No edge caching
  - No one-off jobs
  - No shell access via SSH or dashboard
  - No private network traffic
  - Cannot listen on reserved ports (18012, 18013, 19099)
  - Cannot send outbound traffic on SMTP ports (25, 465, 587)

### Free PostgreSQL Databases
- **Single instance limit**: Only one free database per workspace.
- **1 GB storage limit**: Fixed capacity.
- **30-day expiration**: Databases expire 30 days after creation. Upgrade to paid within 14 days of expiration or lose data.
- **Limitations**:
  - No maintenance windows (may restart anytime)
  - No backups

### Free Key Value Instances
- **Single instance limit**: Only one free instance per workspace.
- **Ephemeral storage**: Data is lost on restarts.
- **Limitations**:
  - No maintenance windows (may restart anytime)
  - Data lost on upgrades to paid plans

**Note**: Free instances are not suitable for production applications. For production, upgrade to paid plans.

## Step 1: Push Code to GitHub

Since Git is not installed locally, you'll need to:

1. **Download and install Git** from https://git-scm.com/downloads
2. **Create a GitHub repository** named `ikr-plantations`
3. **Initialize Git in your project**:
   ```bash
   git init
   git add .
   git commit -m "image and static files rendering"
   git branch -M main  # Renames the default branch to 'main'
   git remote add origin https://github.com/ghostketm/ikr-plantations.git
   git push -u origin main
   ```

## Step 2: Deploy on Render.com

### Option A: Using render.yaml (Recommended)

1. **Go to Render.com** and sign in
2. **Click "New"** → **"Blueprint"**
3. **Connect your GitHub repository** (`ikr-plantations`)
4. **Render will automatically detect** `render.yaml` and set up:
   - Web service with Python runtime
   - PostgreSQL database
   - All environment variables

### Option B: Manual Setup

If render.yaml doesn't work:

1. **Create PostgreSQL Database**:
   - Go to Render Dashboard → New → PostgreSQL
   - Name: `ikr-db`
   - Copy the connection string

2. **Create Web Service**:
   - Go to Render Dashboard → New → Web Service
   - Connect your GitHub repo
   - Settings:
     - **Name**: `ikr-plantations`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
     - **Start Command**: `gunicorn ikr_project.wsgi:application --bind 0.0.0.0:$PORT`

3. **Environment Variables**:
   ```
   DJANGO_SETTINGS_MODULE=ikr_project.settings.production
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   DATABASE_URL=postgresql://user:password@host:5432/dbname  # From your PostgreSQL instance
   ALLOWED_HOSTS=https://ikr-plantations.onrender.com
   ```

## Step 3: Post-Deployment Setup

After deployment, you'll need to create a superuser:

1. **Open Render service shell** or use the command:
   ```bash
   # If you have Render CLI installed:
   render run --service ikr-plantations python manage.py createsuperuser
   ```

2. **Or temporarily add this to your build command** (remove after first deploy):
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('ikrADMIN', 'ghostketm@gmail.com', 'QWERTY123$%^&*()')" | python manage.py shell
   ```

## Step 4: Access Your Application

- **Live Site**: `https://ikr-plantations.onrender.com`
- **Admin Panel**: `https://ikr-plantations.onrender.com/admin/`
- **Default Admin Credentials**: admin / admin123 (change immediately!)

## Step 5: Domain Configuration (Optional)

To use a custom domain:
1. Go to your Render web service settings
2. Add your custom domain
3. Update DNS records as instructed
4. Update `ALLOWED_HOSTS` environment variable

## Troubleshooting

### Build Failures
- Check build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility

### Database Connection Issues
- Confirm `DATABASE_URL` is correct
- Check PostgreSQL instance is running
- Verify database credentials

### Static Files Not Loading
- Ensure `collectstatic` ran during build
- Check `STATIC_URL` and `STATIC_ROOT` settings

### 500 Errors
- Check application logs
- Verify environment variables
- Ensure migrations ran successfully

## Security Checklist

- [ ] Change default admin password
- [ ] Set strong `SECRET_KEY`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Enable HTTPS (Render does this automatically)
- [ ] Set up email configuration for production
- [ ] Configure media file storage if needed

## Performance Optimization

- Enable Render's free SSL
- Consider upgrading to paid plan for better performance
- Set up monitoring and alerts
- Configure backup strategy for PostgreSQL

## Next Steps

1. **Test all functionality** on the live site
2. **Set up monitoring** with Render's built-in tools
3. **Configure email** for user notifications
4. **Add more content** through the admin panel
5. **Set up analytics** (Google Analytics, etc.)

---

**Need Help?** Check Render's documentation or contact their support.
