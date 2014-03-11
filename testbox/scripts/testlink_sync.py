"""
Sync testcases/testsuites from testlink

Todo:
    1.develop a interface in testlink for testbox
"""
import os
import logging
from testlink import TestlinkAPIClient, TestLinkHelper
from testbox import create_app

logging.basicConfig(level=logging.DEBUG)

os.environ['TESTLINK_API_PYTHON_SERVER_URL'] = ''
os.environ['TESTLINK_API_PYTHON_DEVKEY'] = ''

_testlink = TestLinkHelper()
_client = _testlink.connect(TestlinkAPIClient)

def _load_locale_nodes():
    resultset = NodesHierarchy.query.filter(NodesHierarchy.node_type_id==2 or NodesHierarchy.node_type_id==3)
    return dict([(node['id'], (node['parent_id'], node['node_order'], node['name'])) for node in resultset])


def _load_remote_nodes(ts_id, remote_nodes=[]):
    testcases = _client.getTestCasesForTestSuite(ts_id, False, 'summary')
    print testcases
    remote_nodes += testcases
    testsuites = _client.getTestSuitesForTestSuite(ts_id)
    print testsuites
    if testsuites:
        if 'name' not in testsuites:
            for ts_id in testsuites:
                ts = _client.getTestSuiteByID(ts_id)
                print ts['name']
                remote_nodes.append(ts)
                _load_remote_nodes(ts_id, remote_nodes)
        else:
            remote_nodes.append(testsuites)


def sync_testproject(tp_id):
    import time
    bf = time.time()
    locale_nodes = {}
    remote_nodes = []
    update_nodes = {'insert': [], 'delete': [], 'update': []}

    first_level_testsuites = _client.getFirstLevelTestSuitesForTestProject(tp_id)
    for ts in first_level_testsuites:
        print ts['name']
        remote_nodes.append(ts)
        _load_remote_nodes(ts['id'], remote_nodes)

    for tc in remote_nodes:
        print tc
        if int(tc['node_type_id']) == 2 or (int(tc['node_type_id']) == 3 and int(tc['execution_type']) == 2):
            try:
                node = locale_nodes.pop(int(tc['id']))
                parent_id, node_order, name = node
                if parent_id != int(tc['parent_id']) or node_order != int(tc['node_order']) or name != int(
                    tc['name']):    # Update
                    update_nodes['update'].append(tc)
            except KeyError:    # Insert
                update_nodes['insert'].append(tc)
        else:
            pass

    update_nodes['delete'] += locale_nodes.keys()   # Delete
    ft = time.time() - bf
    print ft

    for handler in update_nodes:
        if handler == 'insert':
            for node in update_nodes['insert']:
                nh = NodesHierarchy()
                nh.id = int(node['id'])
                nh.name = node['name']
                nh.parent_id = int(node['parent_id'])
                nh.node_type_id = int(node['node_type_id'])
                nh.node_order = int(node['node_order'])
                db.session.add(nh)
        elif handler == 'delete':
            pass
        elif handler == 'update':
            pass


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        from testbox.models import db, SystemConfig, UserConfig, NodesHierarchy, TestCase

        sync_testproject(1)
