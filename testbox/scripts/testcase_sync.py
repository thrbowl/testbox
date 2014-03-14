"""
Sync testcases/testsuites from testlink

Todo:
    1.develop a interface in testlink for testbox
"""
import os
import logging
from sqlalchemy import or_
from testlink import TestlinkAPIClient, TestLinkHelper
from testbox import create_app

logging.basicConfig(level=logging.INFO)

NODE_TESTSUITE = 2
NODE_TESTCASE = 3

EXECUTION_MANUAL = 1
EXECUTION_AUTOMATED = 2

def _load_locale_nodes():
    resultset = NodesHierarchy.query.filter(or_(NodesHierarchy.node_type_id == NODE_TESTSUITE,
        NodesHierarchy.node_type_id == NODE_TESTCASE))
    return dict([(node.id, node) for node in resultset])


class Database(object):
    @staticmethod
    def insert(node):
        ob = NodesHierarchy(node['name'], int(node['parent_id']), int(node['node_type_id']))
        ob.id = int(node['id'])
        ob.node_order = int(node['node_order'])
        db.session.add(ob)
        if int(node['node_type_id']) == NODE_TESTCASE:
            tc = TestCase(int(node['id']), node['external_id'], '%s.py' % node['name'])
            db.session.add(tc)

    @staticmethod
    def delete(node):
        ob = NodesHierarchy.query.get(node.id)
        db.session.delete(ob)
        if node.node_type_id == NODE_TESTCASE:
            tc = TestCase.query.filter(TestCase.id == node.id).one()
            db.session.delete(tc)

    @staticmethod
    def update(node):
        ob = NodesHierarchy.query.get(int(node['id']))
        ob.name = node['name']
        ob.parent_id = int(node['parent_id'])
        ob.node_order = int(node['node_order'])
        db.session.add(ob)


def sync_testcases(tp_id):
    all_testsuites = {}
    locale_nodes = _load_locale_nodes()
    update_nodes = {'insert': [], 'delete': [], 'update': []}

    # Get all testcases and testsuites from testlink
    first_level_testsuites = _client.getFirstLevelTestSuitesForTestProject(tp_id)
    remote_nodes = []
    for ts in first_level_testsuites:
        all_testsuites[int(ts['id'])] = ts
        remote_nodes += _client.getTestCasesForTestSuite(ts['id'], True, 'level')

    # Extract directly used testsuites and automated testcases
    direct_used_testsuites = set()
    automated_testcases = []
    for rnode in remote_nodes:
        if int(rnode['node_type_id']) == NODE_TESTCASE and int(rnode['execution_type']) == EXECUTION_AUTOMATED:
            direct_used_testsuites.add(int(rnode['parent_id']))
            automated_testcases.append(rnode)
        elif int(rnode['node_type_id']) == NODE_TESTSUITE:
            all_testsuites[int(rnode['id'])] = rnode

    # Get all used testsuites
    all_used_testsuites = set()

    def _add_parent_testsuites(ts_id):
        all_used_testsuites.add(ts_id)
        ts = all_testsuites[ts_id]
        if int(ts['parent_id']) != tp_id:
            _add_parent_testsuites(int(ts['parent_id']))

    for ts_id in direct_used_testsuites:
        _add_parent_testsuites(ts_id)

    # Merge testsuites and testcases for update
    automated_testcases += [all_testsuites[ts_id] for ts_id in all_used_testsuites]

    # Compared with locale data
    for rnode in automated_testcases:
        try:
            lnode = locale_nodes.pop(int(rnode['id']))
            if lnode.parent_id != int(rnode['parent_id'])\
               or lnode.node_order != int(rnode['node_order'])\
            or lnode.name != rnode['name']:    # Update
                update_nodes['update'].append(rnode)
        except KeyError:    # Insert
            update_nodes['insert'].append(rnode)
    update_nodes['delete'] += locale_nodes.values()   # Delete

    #from pprint import pprint
    #pprint(update_nodes)

    # Update databases
    for handler in update_nodes:
        func = getattr(Database, handler)
        for node in update_nodes[handler]:
            func(node)


if __name__ == '__main__':
    import time

    start = time.time()
    app = create_app()
    with app.app_context():
        from testbox.models import db, SystemConfig, NodesHierarchy, TestCase

        os.environ['TESTLINK_API_PYTHON_SERVER_URL'] = 'http://localhost/testlink-1.9.3/lib/api/xmlrpc.php'
        os.environ['TESTLINK_API_PYTHON_DEVKEY'] = '6f1f44328eca4915c94c5baff5a9d1ea'
        _testlink = TestLinkHelper()
        _client = _testlink.connect(TestlinkAPIClient)
        sync_testcases(1)
        try:
            db.session.commit()
        except:
            db.session.rollback()
    end = time.time()
    logging.info(end - start)
