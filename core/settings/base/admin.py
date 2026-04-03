class BaseAdminSettings:
    def get_admin_password(self) -> str:
        raise NotImplementedError

    def validate_admin_password(self, input_var) -> bool:
        raise NotImplementedError
