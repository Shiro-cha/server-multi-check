class InstallIdentityUseCase:
    def __init__(self, identity_service):
        self.identity_service = identity_service

    def execute(self):
        return self.identity_service.install_identity()