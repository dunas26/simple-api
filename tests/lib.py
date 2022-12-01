from httpx import Response


class BaseTest:
    @fixture(autouse=True)
    def before_each(self):
        # Restore the service base data
        service.data = base_data


def is_allowed_method(res: Response):
    return res.status_code != 405


def has_been_found(res: Response):
    return res.status_code != 404


def is_response_ok(res: Response):
    return res.status_code == 200


def unauthorized(res: Response):
    return res.status_code == 401


def not_found(res: Response):
    return res.status_code == 404


def unprocessable_entity(res: Response):
    return res.status_code == 422
