import mongoengine
import ssl
alias_core = 'core'
db = 'sportcompanion'

# data = dict(
# 	username = user_from_config_or_env, 
# 	password = password_from_config_or_env,
# 	host = server_from_config_or_env,
# 	port = port_from_config_or_env,
# 	authentication_source = 'admin',
# 	authentication_mechanism = "SCRAM-SHA-1",
# 	ssl = True,
# 	ssl_cert_reqs = ssl.CERT_NONE)

#def global_init():
#	mongoengine.register_connection(alias = "core", name='sport_companion')

def global_init(user=None, password=None, port=27017, server='localhost', use_ssl=True, db_name='sport_companion'):
    if user or password:
        data = dict(
            username=user,
            password=password,
            host=server,
            port=port,
            authentication_source='admin',
            authentication_mechanism='SCRAM-SHA-1',
            ssl=use_ssl,
            ssl_cert_reqs=ssl.CERT_NONE)
        mongoengine.register_connection(alias='core', name=db_name, **data)
        data['password'] = '*************'
        print(" --> Registering prod connection: {}".format(data))
    else:
        print(" --> Registering dev connection")
        mongoengine.register_connection(alias='core', name=db_name)