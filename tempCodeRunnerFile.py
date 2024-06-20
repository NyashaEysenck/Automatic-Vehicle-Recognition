from website import create_app, DB

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        DB.create_all()
    app.run(debug=True)  
