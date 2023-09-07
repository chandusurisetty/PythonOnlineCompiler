from io import StringIO
from contextlib import redirect_stdout
from flask import jsonify
import traceback


class Analay:
    def __init__(self, code):
        self.code = code

    def solution(self):
        output = StringIO()

        with redirect_stdout(output):

            try:

                exec(self.code)
                return {"message": output.getvalue()}
            except Exception as e:
                error = traceback.format_exc()

                return {"message": error}
