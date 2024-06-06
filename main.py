import os
from app import create_app

from werkzeug.security import generate_password_hash, check_password_hash

print(generate_password_hash("1234567890"))

app = create_app()

if __name__ == "__main__":
    debug_mode = os.getenv('FLASK_DEBUG', 'True') == 'True'
    print('run')
    app.run(debug=debug_mode, port=5000)
