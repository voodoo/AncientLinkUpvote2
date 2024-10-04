from app import create_app
from seed import seed_database
import sys
from urllib.parse import urlparse

app = create_app()
app.jinja_env.globals.update(urlparse=urlparse)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--seed":
        with app.app_context():
            seed_database()
    elif app.config.get('DEBUG', False):
        with app.app_context():
            seed_database()
    app.run(host="0.0.0.0", port=5000)
