from app import create_app
from seed import seed_database
import sys

app = create_app()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--seed":
        with app.app_context():
            seed_database()
    else:
        app.run(host="0.0.0.0", port=5000)
