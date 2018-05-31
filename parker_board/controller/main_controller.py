from flask import Blueprint
from parker_board.schema.board import boards_schema
from parker_board.model.board import Board


bp = Blueprint('main', __name__)


@bp.route('/')
def main():
    boards = Board.query.all()
    return boards_schema.jsonify(boards), 200
