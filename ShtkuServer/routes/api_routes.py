import sys
sys.path.append('../')
from controllers.api_controller import *

def set_routes(app):
    @app.route('/')
    def route_get_records1():
        return get_records1()

    @app.route('/show')
    def route_show_records():
        return show_records()

    @app.route('/getrecords', methods=['GET'])
    def route_fetch_all_questions():
        return fetch_all_questions()

    @app.route('/getevaluatrecords', methods=['GET'])
    def route_fetch_all_evaluation_results():
        return fetch_all_evaluation_results()

    @app.route('/add', methods=['POST'])
    def route_add_or_update_question_records():
        return add_or_update_question_records()

    @app.route('/evaluator', methods=['POST'])
    def route_evaluate_answers():
        return evaluate_answers()

    @app.route('/deleteall', methods=['GET'])
    def route_delete_all_questions():
        return delete_all_questions()

    @app.route('/deletebyid', methods=['POST'])
    def route_delete_question_by_id():
        return delete_question_by_id()

