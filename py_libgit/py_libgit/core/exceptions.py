class FileNamingConventionError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class NotGitRepoError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class BlobHashConflictError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
