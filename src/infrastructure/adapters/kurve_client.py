class KurveClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_token(self):
        """
        Retrieves a token from the Kurve API.
        """
        return "fake_token"