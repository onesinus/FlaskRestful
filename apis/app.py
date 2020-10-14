from . import create_app
from .db import init_app

app = create_app()
init_app(app)
app.run()