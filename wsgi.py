from apis import create_app
from apis.db import init_db

init_db()

app = create_app()