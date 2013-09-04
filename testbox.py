import os
from flask import Flask, render_template


def create_app(name=None, settings=None):
    """http://flask.pocoo.org/docs/patterns/appfactories/
    """
    if name is None:
        name = __name__

    app = Flask(name)

    default_settings = os.path.join(app.root_path, 'settings.cfg')
    app.config.from_pyfile(default_settings)
    if settings is not None:
        app.config.from_object(settings)
    app.config.from_envvar('TESTBOX_SETTINGS', silent=True)

    #TODO *register blueprint to application*

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    return app
