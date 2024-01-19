from core import create_app

app = create_app()

if __name__ == '__main__':
    # degub = False in production.
    app.run(debug=True)