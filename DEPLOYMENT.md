# SMS Spam Detector - Deployment Guide

## Render Deployment (Backend)

### Prerequisites
- Render account (free tier available)
- GitHub repository with your code

### Steps to Deploy

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the `backend` folder as root directory
   - Use these settings:
     - **Name**: sms-spam-detector-api
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Health Check Path**: `/health`

3. **Environment Variables** (if needed)
   - `PYTHON_VERSION`: 3.9.16

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete
   - Your API will be available at: `https://sms-spam-detector-api.onrender.com`

## Vercel Deployment (Frontend)

### Prerequisites
- Vercel account (free tier available)
- GitHub repository with your code

### Steps to Deploy

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy Frontend**
   ```bash
   cd frontend
   vercel --prod
   ```

3. **Set Environment Variable**
   - In Vercel dashboard, add environment variable:
   - `BACKEND_URL`: `https://your-render-app-url.onrender.com`

4. **Redeploy**
   ```bash
   vercel --prod
   ```

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## Troubleshooting

### Common Issues

1. **Model files not found**
   - Ensure `model.pkl` and `vectorizer.pkl` are in the backend folder
   - Check file paths in `main.py`

2. **CORS errors**
   - Backend CORS is configured to allow all origins
   - For production, update to your specific frontend domain

3. **NLTK data download**
   - Build script downloads required NLTK data
   - Check build logs for download errors

4. **Port issues**
   - Render uses `$PORT` environment variable
   - Local development uses port 8000

### Testing

1. **Backend Health Check**
   ```bash
   curl https://your-app.onrender.com/health
   ```

2. **Frontend Connection**
   - Open frontend in browser
   - Check backend status indicator
   - Test with sample email text

## Production URLs

After deployment:
- Backend API: `https://sms-spam-detector-api.onrender.com`
- Frontend App: `https://your-vercel-app.vercel.app`
- API Documentation: `https://sms-spam-detector-api.onrender.com/docs`
