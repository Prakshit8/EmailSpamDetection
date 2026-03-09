# SMS Spam Detector - Streamlit Deployment Guide

## Deploy on Streamlit Community Cloud

### Prerequisites
- Streamlit account (free)
- GitHub repository with your code

### Steps to Deploy

1. **Go to Streamlit Community Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Connect Your Repository**
   - Click "New app" 
   - Select repository: `Prakshit8/EmailSpamDetection`
   - Select branch: `main`
   - Select main file path: `frontend/app.py`

3. **Configure Settings**
   - **App name**: SMS Spam Detector
   - **App URL**: sms-spam-detector
   - **Python version**: 3.9
   - **Dependencies**: `frontend/requirements.txt`

4. **Set Environment Variables**
   - Go to "Advanced settings"
   - Add environment variable:
     - **Name**: `BACKEND_URL`
     - **Value**: `https://your-render-app-url.onrender.com`

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be available at: `https://sms-spam-detector.streamlit.app`

### After Backend Deployment

Once you deploy your backend on Render:
1. Get your Render URL: `https://sms-spam-detector-api.onrender.com`
2. Update the `BACKEND_URL` environment variable in Streamlit
3. Redeploy the Streamlit app

### Local Testing

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### Troubleshooting

1. **Backend Connection Error**
   - Ensure backend is deployed and running
   - Check `BACKEND_URL` environment variable
   - Verify CORS settings on backend

2. **Import Errors**
   - Check requirements.txt has correct versions
   - Verify Python version compatibility

3. **Deployment Issues**
   - Check Streamlit logs for errors
   - Ensure all files are in GitHub repo
   - Verify file paths are correct

### Features

- ✅ Professional dark theme UI
- ✅ Real-time email analysis
- ✅ Error handling and fallbacks
- ✅ Responsive design
- ✅ Production-ready configuration
