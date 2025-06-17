from flask import Flask, render_template

def create_app():
    """
    Factory function untuk membuat dan mengonfigurasi aplikasi Flask.
    """
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')

    with app.app_context():
        from .routes import main_api

        app.register_blueprint(main_api)

        @app.route('/')
        def index():
            """Menyajikan halaman index.html."""
            return render_template('index.html')

    return app
