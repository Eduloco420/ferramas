from flask import Blueprint
from app.controllers.orchestrator_controller import OrchestratorController

root_bp = Blueprint('root_bp', __name__)
orchestrator_controller = OrchestratorController()

@root_bp.route('/', methods=['GET'])
def home():
    return orchestrator_controller.home()

@root_bp.route('/ms_status', methods=['GET'])
def ms_status():
    return orchestrator_controller.ms_status()