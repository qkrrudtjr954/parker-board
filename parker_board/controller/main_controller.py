from flask import Blueprint, request
from parker_board.schema.board import main_boards_schema
from parker_board.model.board import Board
from parker_board.schema.resp import resp_schema


bp = Blueprint('main', __name__)


@bp.route('/')
def main():
    result = {}
    boards = Board.query.filter(Board.status != 2).order_by(Board.created_at.desc()).paginate(per_page=3, error_out=False)
    page = int(request.args.get('page')) if request.args.get('page') else 1
    boards.page = page

    data = {}
    data['boards'] = main_boards_schema.dump(boards.items).data
    data['pagination'] = dict(total=boards.total, page=boards.page, has_next=boards.has_next, has_prev=boards.has_prev)
    result['data'] = data

    return resp_schema.jsonify(result), 200
