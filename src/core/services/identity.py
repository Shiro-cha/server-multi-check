class IdentityService:
    def __init__(self,config):
        self.config = config
    def install_identity(self):
        server_config = self.config.load_config("servers")
        print(server_config)
        return "Identity installed"