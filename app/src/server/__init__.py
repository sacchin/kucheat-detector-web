from flask import Flask, render_template
from . import detector


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.default')


@app.route('/index')
def index():
    return render_template('index.html')


# blueprints = [detector]
# for blueprint in blueprints:
#     app.register_blueprint(blueprint.app)
