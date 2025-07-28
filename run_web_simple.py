#!/usr/bin/env python3
"""
Launch the web-based chess game (simplified version)
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
    print("🚀 Starting AI Chess Web Game (Simple Version)...")
    print("📡 Server will start at http://localhost:5000")
    print("🤖 Using random AI (no ML model required)")
    
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
        
        from app_simple import app
        print("✅ Server starting...")
        print("🌐 Open http://localhost:5000 in your browser")
        print("⏹️  Press Ctrl+C to stop the server")
        
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()