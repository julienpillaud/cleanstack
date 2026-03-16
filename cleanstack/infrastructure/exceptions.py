from cleanstack.domain import UnprocessableEntityError


class RepositoryError(Exception):
    pass


class InvalidFieldError(RepositoryError, UnprocessableEntityError):
    pass


class InvalidFilterError(RepositoryError, UnprocessableEntityError):
    pass
