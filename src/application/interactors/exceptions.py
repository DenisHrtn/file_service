from base_exception import BaseAppException


class EmptyFilenameException(BaseAppException):
    def __init__(self):
        super().__init__("Filename cannot be empty", 400)


class FileDoesNotExistException(BaseAppException):
    def __init__(self):
        super().__init__("File does not exists", 400)


class EmptyFileTypeException(BaseAppException):
    def __init__(self):
        super().__init__("File type cannot be empty", 400)
