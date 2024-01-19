from .exceptions import FyleError


def base_assert(error_code, msg):
    """
    Base assertion function.
    """
    raise FyleError(status_code=error_code, message=msg)


def assert_auth(cond, msg='UNAUTHORIZED'):
    """
    Assert that the user is authenticated.
    """
    
    if cond is False:
        base_assert(401, msg)


def assert_true(cond, msg='FORBIDDEN'):
    """
    Assert that the user is authorized.
    """
    if cond is False:
        base_assert(403, msg)


def assert_valid(cond, msg='BAD_REQUEST'):
    """
    Assert that the request is valid.
    """
    if cond is False:
        base_assert(400, msg)


def assert_found(_obj, msg='NOT_FOUND'):
    """
    Assert that the object exists.
    """
    if _obj is None:
        base_assert(404, msg)
