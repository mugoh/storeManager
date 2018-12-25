<<<<<<< HEAD
from app.api.v1 import create_app

#config = os.getenv('APP_SETTINGS')
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
=======
from app import app

if __name__ == '__main__':
	app.my_app.run()
>>>>>>> master
