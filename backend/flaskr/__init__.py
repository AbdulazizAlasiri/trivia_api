#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

QUESTIONS_PER_PAGE = 10


def paginate_question(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


# Returns a unique and random question that has not been used in previous_questions
def random_unique_question(questions, previous_questions):
    questions = [question.format() for question in questions]
    unique_questions = [
        question for question in questions if question['id'] not in previous_questions]
    if len(unique_questions) == 0:
        return None
    random_index = random.randrange(0, len(unique_questions))
    rondom_question = unique_questions[random_index]
    return rondom_question
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # CORS(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,DELETE')
        return response
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

#  Categories
#  ----------------------------------------------------------------
    @app.route('/categories')
    def retrieve_categories():
        category_selection = Category.query.order_by(Category.id).all()
        categories = {cat.id: cat.type for cat in category_selection}
        if len(category_selection) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories
        })

    @app.route('/categories/<int:category_id>/questions')
    def get_by_category(category_id):

        question_selection = Question.query.filter(
            Question.category == category_id).all()
        current_question = paginate_question(
            request, question_selection)
        if len(current_question) == 0 and question_selection:
            abort(404)
        else:
            print({
                'success': True,
                'questions': current_question,
                'total_questions': len(question_selection),
                'current_category': category_id
            })
            return jsonify({
                'success': True,
                'questions': current_question,
                'total_questions': len(question_selection),
                'current_category': category_id
            })


#  Questions
#  ----------------------------------------------------------------

    @app.route('/questions')
    def retrieve_questions():
        question_selection = Question.query.order_by(Question.id).all()
        current_question = paginate_question(request, question_selection)

        category_selection = Category.query.order_by(Category.id).all()
        categories = {cat.id: cat.type for cat in category_selection}
        if len(current_question) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': current_question,
            'total_questions': len(question_selection),
            'categories': categories,
            'current_category': None
            #  list(dict.fromkeys([question['category'] for question in current_question]))

        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
        except:
            abort(422)
        if question is None:
            abort(404)

        question.delete()

        return jsonify({
            'success': True,
            'deleted': question_id,
        })

# this method to create a question and to search for one
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)
        searchTerm = body.get('searchTerm', None)

        if not searchTerm is None:
            try:
                question_selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(searchTerm)))

                current_question = paginate_question(
                    request, question_selection)

            except:
                abort(422)

            return jsonify({
                'success': True,
                'questions': current_question,
                'total_questions': len(question_selection.all()),
                'currentCategory': None
            })

        else:
            # i would midfay the model for not allowing nulls,but i am not sure if that is a part of the project
            if not new_question or not new_answer or not new_difficulty or not new_category:
                abort(400)

            question = Question(question=new_question, answer=new_answer,
                                difficulty=new_difficulty, category=new_category)

            question.insert()

            return jsonify({
                'success': True,
                'created': question.id,
            })


#  Quizzes
#  ----------------------------------------------------------------

    @app.route('/quizzes', methods=['POST'])
    def create_quizzes():
        body = request.get_json()
        try:
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)

            if quiz_category['id'] == 0:
                question_selection = Question.query.all()
                next_question = random_unique_question(
                    question_selection, previous_questions)

            else:
                question_selection = Question.query.filter(
                    Question.category == quiz_category['id']).all()

                if len(question_selection) == 0:
                    abort(404)

                next_question = random_unique_question(
                    question_selection, previous_questions)

        except:
            abort(422)
        return jsonify({
            'success': True,
            'question': next_question,
        })

#----------------------------------------------------------------------------#
# Errors.
#----------------------------------------------------------------------------#
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app
