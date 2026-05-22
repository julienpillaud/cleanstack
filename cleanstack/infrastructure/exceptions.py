from cleanstack.domain import UnprocessableContentError


class RepositoryError(Exception):
    pass


class InvalidFieldError(RepositoryError, UnprocessableContentError):
    pass


class InvalidFilterError(RepositoryError, UnprocessableContentError):
    pass
