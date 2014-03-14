import ldap
from flask import redirect, current_app

ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)


def ldap_verify_user(uid, password):
    try:
        l = ldap.initialize(current_app.config['LDAP_SERVICE_URL'])
        l.simple_bind_s(current_app.config['LDAP_PEOPLE_DN'] % uid, password)
        l.unbind_s()
        return True
    except ldap.LDAPError:
        return False


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
        l.unbind_s()
        return dict([(k, result_set[0][0][1][k][0]) for k in attrs])
    except ldap.LDAPError:
        return None
