#!/usr/bin/env python3
"""
Launch script for VLM Demo Application
Automatically handles dependencies and setup
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Check if all required packages are installed"""
    required = [
        'gradio',
        'openai',
        'anthropic',
        'dotenv',
        'PIL',
        'sqlalchemy'
    ]

    missing = []
    for package in required:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            elif package == 'PIL':
                __import__('PIL')
            else:
                __import__(package)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"⚠️  Missing dependencies: {', '.join(missing)}")
        print("📦 Installing missing packages...")
        os.system(f"{sys.executable} -m pip install -q {' '.join(missing)}")

def main():
    """Main entry point"""
    print("🎨 VLM Demo Application - Complete Edition")
    print("=" * 60)

    # Check dependencies
    check_dependencies()

    # Import and run
    try:
        from app_complete import create_comprehensive_ui
        print("✅ Loading application...")

        demo = create_comprehensive_ui()
        port = int(os.getenv("APP_PORT", 7860))

        print(f"🚀 Starting server on port {port}...")
        print(f"📍 Open your browser to: http://localhost:{port}")
        print("Press Ctrl+C to stop")
        print("=" * 60)

        demo.launch(
            server_name="0.0.0.0",
            server_port=port,
            share=False,
            show_error=True
        )

    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Check that all dependencies are installed: pip install -r requirements.txt")
        print("2. Verify your .env file is configured")
        print("3. Try running: python app_complete.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
