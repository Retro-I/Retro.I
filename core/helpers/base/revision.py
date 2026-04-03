class BaseRevisionHelper:
    def get_branches(self) -> list[dict]:
        raise NotImplementedError

    def get_local_branches(self):
        raise NotImplementedError

    def get_tags(self) -> list[dict]:
        raise NotImplementedError

    def get_current_revision(self) -> str:
        raise NotImplementedError

    def cleanup_local_branches(self):
        raise NotImplementedError
