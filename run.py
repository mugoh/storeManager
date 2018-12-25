from app import api

app = api.app_instance('development')

if __name__ == '__main__':
	app.run(debug=True)
