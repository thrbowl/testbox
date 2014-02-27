import os
from datetime import timedelta

# Major.Minor.Revision
VERSION = '1.0'

# Cookie secret
SECRET_KEY = 'dX6mg0jx0y`8(F_|Cp(#zUQTSAX_y<Q0%^W*#Q7<Wwyb2$^9DB4f<J>7Q~*#{&F~'

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'mysql://b43258:b43258@localhost/testbox'
SQLALCHEMY_ECHO = True
SQLALCHEMY_RECORD_QUERIES = False
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_POOL_TIMEOUT = 10
SQLALCHEMY_POOL_RECYCLE = 2 * 60 * 60
