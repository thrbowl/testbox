import os, logging
from flask import Flask, render_template, url_for

try:
    import pkg_resources
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = '<unknown>'


def create_app(name=None, settings=None):
    """http://flask.pocoo.org/docs/patterns/appfactories/"""
    app = Flask(name or __name__)

    # register settings
    # priority: env variable > params > settings.cfg
    app.config.from_pyfile('settings.cfg')
    if settings is not None:
        if isinstance(object, settings):
            app.config.from_object(settings)
        elif os.path.isfile(os.path.join(app.root_path, settings)):
            app.config.from_pyfile(settings)
    app.config.from_envvar('TESTBOX_SETTINGS', silent=True)

    logging.debug('register blueprints to app')
    from .views.main import main
    app.register_blueprint(main)
    from .views.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    logging.debug('add global templates function')
    app.jinja_env.globals['static'] = (lambda filename: url_for('static', filename=filename))

    @app.errorhandler(404)
    def http404(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def http500(error):
        return render_template('500.html'), 500

    return app
