from project.config import config
from project.models import Genre
from project.server import create_app, db

app = create_app(config)


if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)

