import os
from pprint import pprint
import redis
from testlink import TestlinkAPIClient, TestLinkHelper

os.environ['TESTLINK_API_PYTHON_SERVER_URL'] = ''
os.environ['TESTLINK_API_PYTHON_DEVKEY'] = ''

_testlink = TestLinkHelper()
_client = _testlink.connect(TestlinkAPIClient)


def sync_testsuite(ts_id):
    first_level_testsuites = _client.getFirstLevelTestSuitesForTestProject(ts_id)
    for ts in first_level_testsuites:
        testcases = _client.getTestCasesForTestSuite(ts['id'], True, 'summary')
        print testcases
        for tc in testcases:
            if tc['node_type_id'] != '3':
                print tc['external_id']
            #if tc['execution_type'] == 2:   #  Automated
            #    pass


def sys_testcase(tc_id):
    pass



if __name__ == '__main__':
    sync_testsuite(1)
