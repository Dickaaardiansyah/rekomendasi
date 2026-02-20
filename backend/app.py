"""
SPK Pemilihan Mata Pelajaran Peminatan
Flask Application Entry Point - v2.0
"""

import os
import sys

# Pastikan backend package dapat di-import
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.api import api

# ─── App Factory ──────────────────────────────────────────────────────────────

def create_app():
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    app = Flask(__name__, static_folder=frontend_path, static_url_path='')
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(api)

    # Serve frontend
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def catch_all(path):
        file_path = os.path.join(app.static_folder, path)
        if os.path.isfile(file_path):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    print(f"\n🚀 SPK Mapel v2.0 berjalan di http://localhost:{port}\n")
    app.run(host='0.0.0.0', port=port, debug=debug)