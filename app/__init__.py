from api.app import create_app

def app_instance(app_setting):
	return create_app(app_setting)
