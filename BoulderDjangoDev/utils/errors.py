"""This module contains all error message classes."""

class InvalidStackexchangeAccountType(Exception):
    pass

class InvalidBlogPostObjectError(Exception):
    pass

class InvalidBlogPostFormError(Exception):
    pass

class InvalidCommentFormError(Exception):
    pass

class InvalidViewNameError(Exception):
    pass

class InvalidHttpMessage(Exception):
    pass

class InvalidJSONResponse(Exception):
    pass

class UnspecifiedModelFieldError(Exception):
    pass
