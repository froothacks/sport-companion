import mongoengine

alias_core = 'core'
db = 'sportcompanion'

data = dict(
	username = user_from_config_or_env, 
	password = password_from_config_or_env,
	host = server_from_config_or_env,
	port = port_from_config_or_env,
	authentication_source = 'admin',
	authentication_mechanism = "SCRAM-SHA-1",
	ssl = True,
	ssl_cert_reqs = ssl.CERT_NONE)

def global_init():
	mongoengine.register_connection(alias = "core", name='sport_companion')
