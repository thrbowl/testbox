from flask import Flask, render_template

def create_app(settings=None, name=None):
    """http://flask.pocoo.org/docs/patterns/appfactories/
    """
    if settings is None:
        _s = settings
    else:
        _s = settings

    if name is None:
        name = __name__

    app = Flask(name)
    if not hasattr(app, 'extensions'):
        app.extensions = {}

    app.config.from_object(_s)
    app.config.from_envvar('TESTBOX_SETTINGS')

    #Todo: register blueprint to application

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    return app
