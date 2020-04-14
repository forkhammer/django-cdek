class CDEKException(BaseException):
    def __init__(self, code:str=None, message:str=None, *args, **kwargs):
        super(CDEKException, self).__init__(*args, **kwargs)
        self.code = code
        self.message = message

    def __str__(self):
        return '[%s] %s' % (self.code, self.message)