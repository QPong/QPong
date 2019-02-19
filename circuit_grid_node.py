class CircuitGridNode():
    """Represents a node in the circuit grid"""
    def __init__(self, node_type, radians):
        self.node_type = node_type
        self.radians = radians

    def __str__(self):
        string = 'node_type: ' + str(self.node_type)
        return string
