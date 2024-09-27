class ChatCache:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ChatCache, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.responses = []
            self.initialized = True

    def AddResponse(self, response : str):
        self.responses.append(response)

    def GetResponses(self):
        return str(self.responses)