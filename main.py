import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    print('run')
    app.run(debug=debug_mode, port=5000)
