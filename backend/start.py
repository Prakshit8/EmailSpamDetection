import os
import sys

def main():
    """Simple startup script to verify all dependencies."""
    print("🚀 Starting SMS Spam Detector Backend...")
    
    try:
        # Test imports
        import fastapi
        import uvicorn
        import nltk
        import sklearn
        import numpy
        print("✅ All dependencies imported successfully")
        
        # Download NLTK data
        try:
            nltk.download('stopwords', quiet=True)
            nltk.download('punkt', quiet=True)
            print("✅ NLTK data downloaded")
        except Exception as e:
            print(f"⚠️ NLTK download warning: {e}")
        
        # Import main app
        from main import app
        print("✅ Main app imported successfully")
        
        # Start server
        port = int(os.environ.get("PORT", 8000))
        print(f"🌐 Starting server on port {port}")
        
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=port)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Startup error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
