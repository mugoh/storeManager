from app import create_app

app = create_app('instance.config')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
