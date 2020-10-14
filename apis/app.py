from apis import create_app
from apis.db import init_app

if __name__ == '__main__':
    app = create_app()
    init_app(app)
    app.run()