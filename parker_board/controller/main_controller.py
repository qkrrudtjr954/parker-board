from flask import Blueprint, request
from parker_board.schema.board import main_boards_schema
from parker_board.model.board import Board


bp = Blueprint('main', __name__)


@bp.route('/')
def main():
    boards = Board.query.filter(Board.status != 2).paginate(per_page=3, error_out=False)
    page = int(request.args.get('page')) if request.args.get('page') else 1
    boards.page = page

    return main_boards_schema.jsonify(boards.items), 200
