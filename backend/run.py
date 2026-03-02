"""
Main application entry point
"""
import os
from app import create_app

# Get configuration from environment
config_name = os.getenv('FLASK_ENV', 'development')

# Create Flask app
app = create_app(config_name)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"""
    ╔════════════════════════════════════════════════════════╗
    ║   Smart Attendance & Shortage Predictor API           ║
    ║   Running on: http://localhost:{port}                  ║
    ║   Environment: {config_name}                            ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
