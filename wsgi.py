from apis import create_app, init_db
from apis.db import init_db

init_db()

app = create_app()