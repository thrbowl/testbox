import os
from testbox import create_app


if __name__ == '__main__':
    app = create_app()
    app.secret_key = os.urandom(24)
    app.run(debug=True, host='0.0.0.0')
