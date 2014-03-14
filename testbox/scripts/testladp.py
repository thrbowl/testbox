import os
import logging
from testbox import create_app
import ldap
from flask import redirect, current_app
from pprint import pprint

ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)


def ldap_query_user(uid, *attrs):
    try:
        l = ldap.initialize(current_app.config['LDAP_SERVICE_URL'])
        l.simple_bind_s(current_app.config['LDAP_SERVICE_USER'], current_app.config['LDAP_SERVICE_PASSWORD'])
        ldap_result_id = l.search(current_app.config['LDAP_PEOPLE_BASE_DN'], ldap.SCOPE_SUBTREE, "(uid=%s)" % uid, attrs)
        result_set = []
        while 1:
            result_type, result_data = l.result(ldap_result_id, 0)
            if (result_data == []):
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
            pprint(result_set)
        l.unbind_s()
    except ldap.LDAPError:
        return None

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    import time

    start = time.time()
    app = create_app()
    with app.app_context():
        data = ldap_query_user('b43258', '*')
    end = time.time()
    logging.info(end - start)