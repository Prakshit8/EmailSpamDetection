#!/bin/bash
echo "🚀 Testing deployment setup..."

# Test 1: Check if all files exist
echo "📁 Checking files..."
if [ -f "main.py" ] && [ -f "requirements.txt" ] && [ -f "start.py" ]; then
    echo "✅ All required files exist"
else
    echo "❌ Missing required files"
    exit 1
fi

# Test 2: Check Python version
echo "🐍 Python version:"
python --version

# Test 3: Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Test 4: Test imports
echo "🔍 Testing imports..."
python -c "
import fastapi
import uvicorn
import nltk
import sklearn
import numpy
print('✅ All imports successful')
"

# Test 5: Download NLTK data
echo "📚 Downloading NLTK data..."
python -c "
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
print('✅ NLTK data downloaded')
"

# Test 6: Test main app import
echo "🎯 Testing main app..."
python -c "
try:
    from main import app
    print('✅ Main app imported successfully')
except Exception as e:
    print(f'❌ Main app import failed: {e}')
    exit(1)
"

echo "🎉 All tests passed! Ready for deployment!"
