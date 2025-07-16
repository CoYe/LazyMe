

class BaseHandler:
    """
    Base class for handling interactions with the GPT model.
    This class should be extended to implement specific behavior.
    """

    def __init__(self, config):
        self.config = config

    def handle_message(self, message: str, system_message: str | None = None):
        """
        Handle a message from the user.
        This method should be overridden in subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")
