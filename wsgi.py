from apis import create_app
from apis.db import init_app

app = create_app()
init_app(app)
