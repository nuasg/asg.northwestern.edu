import ldap
from django.conf import settings

con = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
con.set_option(ldap.OPT_NETWORK_TIMEOUT, 10.0)
con.simple_bind_s(settings.AUTH_LDAP_BIND_DN, settings.AUTH_LDAP_BIND_PASSWORD)

def get_ldap_info(netid=None, email=None):
    base_dn = 'dc=northwestern,dc=edu'
    search_scope = ldap.SCOPE_SUBTREE
    retrieve_attributes = None
    if netid:
        search_filter = 'uid=%s' % netid
    elif email:
        search_filter = 'mail=%s' % email
    else:
        return None
    result = con.search_s(base_dn, search_scope, search_filter, retrieve_attributes)
    if result:
        return result[0][1] # the dictionary of attributes
    return None

