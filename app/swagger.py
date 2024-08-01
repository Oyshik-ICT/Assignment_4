from flask import Blueprint, send_from_directory, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

# Set up the blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    '/swagger',  # Swagger UI endpoint
    '/spec',     # Swagger JSON specification endpoint
    config={     # Swagger UI config overrides
        'app_name': "User Management API"
    }
)

swagger = Blueprint('swagger', __name__)

@swagger.route('/spec')
def spec():
    return send_from_directory('.', 'openapi.yaml')  # Serve the YAML spec file
