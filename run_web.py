#!/usr/bin/env python3
"""
Launch the web-based chess game
"""

import os
import sys
import webbrowser
import time
from threading import Timer

def open_browser():
    """Open browser after a short delay"""
    webbrowser.open('http://localhost:5000')

def main():
    print("🚀 Starting AI Chess Web Game...")
    print("📡 Server will start at http://localhost:5000")
    
    # Add current directory to path for imports
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    # Open browser after 2 seconds
    Timer(2.0, open_browser).start()
    
    # Import and run Flask app
    try:
        # Change to web directory and import
        web_dir = os.path.join(current_dir, 'web')
        sys.path.insert(0, web_dir)
        os.chdir(web_dir)
        
        from app import app
        print("✅ Server starting...")
        print("🌐 Open http://localhost:5000 in your browser")
        print("⏹️  Press Ctrl+C to stop the server")
        
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("Make sure you have installed the requirements:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()