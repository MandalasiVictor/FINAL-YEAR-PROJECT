

class ConnectionBase:
    def __init__(self, integration):
        self.integration = integration
        self.connection = None
        
    def connect(self):
        raise NotImplementedError("Subclasses must implement connect() method.")
    
    def get_data(self):
        raise NotImplementedError("Subclasses must implement get_data() method.")
    
