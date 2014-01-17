import datetime
from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, Text, DateTime, func, and_, select
from sqlalchemy.orm import relationship, backref, object_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy(current_app)


