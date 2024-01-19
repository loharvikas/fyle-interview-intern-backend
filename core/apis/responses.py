from flask import Response, jsonify, make_response


class APIResponse(Response):
    """
    API Response class.
    Add additional functionality to the Response class.
    """
    @classmethod
    def respond(cls, data):
        return make_response(jsonify(data=data))
