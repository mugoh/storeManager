from app import create_app

app = create_app('config_setting')

if __name__ == '__main__':
    app.run(debug=True)
