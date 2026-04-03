class BaseRadioMetaHelper:
    def get_song_info(self, url) -> str:
        raise NotImplementedError

    def get_stations_by_name(self, name: str) -> list:
        raise NotImplementedError
