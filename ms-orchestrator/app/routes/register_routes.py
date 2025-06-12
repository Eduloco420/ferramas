from flask import Blueprint
from app.controllers.orchestrator_controller import OrchestratorController

register_bp = Blueprint('register_bp', __name__)
orchestrator_controller = OrchestratorController()

@register_bp.route('', methods=['POST'])
def register():
    return orchestrator_controller.register()
