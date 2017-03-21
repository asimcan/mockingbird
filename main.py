from flask import Flask, g, render_template, request, session, abort



app = Flask(__name__)
app.config.from_object('settings')

from routes.main import main_routes
app.register_blueprint(main_routes)

app.run()
