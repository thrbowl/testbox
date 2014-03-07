import os
from datetime import timedelta

PROJECT_NAME = 'My Testbox'
# Major.Minor.Revision
PROJECT_VERSION = '1.0'
PROJECT_COMPANY = 'Freescale Semiconducto'

# Cookie secret
SECRET_KEY = 'dX6mg0jx0y`8(F_|Cp(#zUQTSAX_y<Q0%^W*#Q7<Wwyb2$^9DB4f<J>7Q~*#{&F~'

# Cache prefix
CACHE_PREFIX = 'testbox_%s_' % PROJECT_VERSION

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'mysql://b43258:b43258@localhost/testbox'
SQLALCHEMY_ECHO = True
SQLALCHEMY_RECORD_QUERIES = False
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_POOL_RECYCLE = 2 * 60 * 60
