import datetime
from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin, AnonymousUserMixin
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, Text, DateTime, func, and_, select
from sqlalchemy.orm import relationship, relation, backref, object_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy(current_app)


def pre_check_privilege(func):
    def _(user_obj, *args, **kwargs):
        if not user_obj.is_active:
            return False
        elif user_obj.is_superuser:
            return True
        else:
            return func(user_obj, *args, **kwargs)

    return _


r_p_association = Table('role_permission', db.metadata,
    Column('id', Integer, primary_key=True),
    Column('role_id', Integer, ForeignKey('role.id'), nullable=False),
    Column('permission_id', Integer, ForeignKey('permission.id'), nullable=False)
)

u_r_association = Table('user_role', db.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('role_id', Integer, ForeignKey('role.id'), nullable=False)
)

u_p_association = Table('user_permissions', db.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id'), nullable=False),
    Column('permission_id', Integer, ForeignKey('permission.id'), nullable=False)
)


class Permission(db.Model):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    description = Column(String(128))

    users = relationship('User', secondary=u_p_association)
    roles = relationship('Role', secondary=r_p_association)


class Role(db.Model):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    description = Column(String(128))

    users = relationship('User', secondary=u_r_association)
    permissions = relationship('Permission', secondary=r_p_association)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    coreid = Column(String(32), nullable=False, unique=True, index=True)
    name = Column(String(32), nullable=False)
    email = Column(String(64), nullable=False)
    _is_active = Column('is_active', Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    last_login = Column(DateTime, nullable=False)
    date_joined = Column(DateTime, nullable=False)

    roles = relationship('Role', secondary=u_r_association)
    permissions = relationship('Permission', secondary=u_p_association)
#    config = relationship('UserConfig', backref('owner'))

    def __init__(self, coreid, name, email):
        self.coreid = coreid
        self.name = name
        self.email = email
        self.date_joined = self.last_login = datetime.datetime.now()
        self._is_active = True

    @classmethod
    def get(cls, coreid):
        try:
            return cls.query.filter(cls.coreid == coreid).one()
        except NoResultFound:
            return None

    def is_active(self):
        return self._is_active

    def disable(self):
        self._is_active = False

    def enable(self):
        self._is_active = True

    def get_all_permissions(self):
        if not hasattr(self, '_perm_cache'):
            if self.is_superuser:
                perms = Permission.query.all()
            else:
                perms = self.permissions + sum([role.permissions for role in self.roles], [])
            self._perm_cache = set([p.permission for p in perms])
        return self._perm_cache

    @pre_check_privilege
    def has_perm(self, perm):
        return perm in self.get_all_permissions()


class UserConfig(db.Model):
    __tablename__ = 'user_config'

    id = Column(Integer, primary_key=True)
    testlink_devkey = Column(String(32), unique=True)

    def __init__(self):
        pass

class NodeTypes(db.Model):
    __tablename__ = 'node_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(String(128))


class NodesHierarchy(db.Model):
    __tablename__ = 'nodes_hierarchy'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    parent_id = Column(Integer, ForeignKey('nodes_hierarchy.id'), nullable=False)
    node_type_id = Column(Integer, nullable=False)
    node_order = Column(Integer)

    children = relationship('NodesHierarchy', backref=backref('parent', remote_side=[id]))

    def __init__(self, name, parent_id, node_type_id):
        self.name = name
        self.parent_id = parent_id
        self.node_type_id = node_type_id


class TestCase(db.Model):
    __tablename__ = 'testcase'

    id = Column(Integer, primary_key=True)
    caseid = Column(String(32), nullable=False, unique=True, index=True)
    script = Column(String(128), nullable=False)
    description = Column(String(128))

    def __init__(self, id, caseid, script):
        self.id = id
        self.caseid = caseid
        self.script = script


class SystemConfig(db.Model):
    __tablename__ = 'system_config'

    id = Column(Integer, primary_key=True)
    testlink_devkey = Column(String(32), unique=True)
    testlink_server_url = Column(String(128))
