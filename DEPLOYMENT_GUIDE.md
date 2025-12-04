# Environment Variable Migration - Complete Guide

## ✅ What I Did

### Files Created:
1. **`config.py`** - New configuration loader that reads from .env or environment variables
2. **`.env`** - Your local environment variables file (contains your actual secrets - DO NOT COMMIT)
3. **`.env.example`** - Template file showing what variables are needed (safe to commit)
4. **`.gitignore`** - Prevents accidentally committing .env to git

### Files Updated:
1. **`app.py`** - Now imports from `config.py` instead of reading `config.json`
2. **`requirements.txt`** - Added `python-dotenv==1.0.0`

### Files Kept (You can delete these later):
- `config.json`
- `config_flask.json`
- `config_respberry_pi.json`

---

## 🚀 How to Deploy on Render

### Step 1: Push to GitHub
```bash
cd C:\Users\Jeremy\Downloads\project\project
git init
git add .
git commit -m "Migrated to environment variables"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Step 2: Create Render Web Service
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: iot-home-security (or whatever you want)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app` (you'll need to add gunicorn to requirements.txt)
   - **Region**: Choose closest to you

### Step 3: Add Environment Variables in Render
In the Render dashboard, go to **Environment** and add these variables (do not store secrets in files):

```
AIO_USERNAME=Jurassicjey
AIO_KEY=REDACTED_AIO_KEY
DATABASE_URL=postgresql://user:password@host/database
FLASK_SECRET_KEY=your-random-secret-key-here
```

**Important**: Generate a strong random secret key for `FLASK_SECRET_KEY` in production!

### Step 4: Deploy
Click "Create Web Service" and Render will automatically deploy your app.

---

## 🔧 Local Development

### To run locally:
```bash
cd C:\Users\Jeremy\Downloads\project\project
python app.py
```

The app will automatically load variables from `.env` file.

### To test production-like environment:
Set environment variables in PowerShell, then run:
```powershell
$env:AIO_USERNAME="Jurassicjey"
$env:AIO_KEY="REDACTED_AIO_KEY"
# ... set other vars ...
python app.py
```

---

## 📝 How It Works

### Development (Local):
1. `config.py` checks if `.env` file exists
2. If yes, loads all variables from `.env`
3. Your app imports from `config.py`

### Production (Render):
1. `.env` file is NOT deployed (it's in `.gitignore`)
2. Render provides environment variables you set in dashboard
3. `config.py` loads from system environment variables
4. Your app works the same way!

---

## 🔒 Security Notes

### ✅ DO:
- Keep `.env` in `.gitignore`
- Use `.env.example` to document required variables
- Set environment variables in Render dashboard
- Use strong random secrets in production

### ❌ DON'T:
- Commit `.env` to git
- Share your `.env` file
- Hardcode secrets in code
- Use the same secrets in dev and production

---

## 🗑️ Optional: Clean Up Old Config Files

Once you verify everything works, you can delete:
- `config.json`
- `config_flask.json`
- `config_respberry_pi.json`

These are no longer needed since all configuration is now in `.env` (local) or Render environment variables (production).

---

## 🐛 Troubleshooting

### App can't find environment variables:
- Check `.env` file exists in the same directory as `config.py`
- Check variable names match exactly (case-sensitive)
- On Render: verify variables are set in dashboard

### Import errors:
```bash
pip install -r requirements.txt
```

### Connection to Raspberry Pi:
The `RSPI_*` variables are optional. Only set them if you need to SSH into your Raspberry Pi from the web server (not common).

---

## 📦 Next Steps (Optional)

1. **Add Gunicorn for production**:
   - Add `gunicorn==21.2.0` to `requirements.txt`
   - Render will use this instead of Flask's development server

2. **Generate strong secret key**:
   ```powershell
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Use this value for `FLASK_SECRET_KEY` in Render

3. **Set up GitHub repository**:
   - Create new repo on GitHub
   - Push your code (`.env` will NOT be pushed thanks to `.gitignore`)

4. **Monitor on Render**:
   - Check logs in Render dashboard
   - Set up health checks
   - Configure custom domain (optional)
