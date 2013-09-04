import logging
logging.basicConfig(level=logging.INFO)

from commands import manager
from testbox import create_app


if __name__ == '__main__':
    manager.app = create_app()
    manager.run()
