from flask import Blueprint
from app.controllers.orchestrator_controller import OrchestratorController

img_bp = Blueprint('img_pb', __name__)
orchestrator_controller = OrchestratorController()

@img_bp.route('/<path:filename>', methods=['GET'])
def ver_imagen(filename):
    return orchestrator_controller.ver_imagen(filename)