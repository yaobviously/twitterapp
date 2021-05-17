from flask import Flask, render_template

def create_app():
    """ Creates and configures an instance of the Flask application """
    app = Flask(__name__)

    app.config("SQLALCHEMY-DATABASE_URI") = "sqlite:///db.sqlite3"
    app.config("SQLALCHEMY-TRACK-MODIFICATIONS") = False
    DB.init_app(app)

    @app.route('/')
    def root():
        users = Users.query.all()
        return render_template("base.html", title = 'Home', users=users)
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        users = Users.query.all()
        

    return app

