from flask import Blueprint
from app.controllers.orchestrator_controller import OrchestratorController

login_bp = Blueprint('login_bp', __name__)
orchestrator_controller = OrchestratorController()

@login_bp.route('/login', methods=['POST'])
def login():
    return orchestrator_controller.login()

@login_bp.route('/token', methods=['POST'])
def validar_token():
    return orchestrator_controller.validar_token()