import os, logging
from flask import Flask, render_template, url_for

try:
    import pkg_resources
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = '<unknown>'


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

    logging.debug('Register blueprints to app')
    from .views.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    logging.debug('Add global templates function')
    app.jinja_env.globals['static'] = (lambda filename: url_for('static', filename=filename))

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    return app
