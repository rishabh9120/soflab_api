from assignment import app
if __name__ == '__main__':
    # session.init_app(app)
    print("app started")
    app.run(debug=True,port=8000)