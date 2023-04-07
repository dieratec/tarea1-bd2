import datetime


class Dataset:
    def __init__(
        self, Id: str = None,  # type: ignore
        name: str = None,  # type: ignore
        description: str = None,  # type: ignore
        user_id: int = None,  # type: ignore
        upload_date: datetime.date = None  # type: ignore
    ):
        self.Id = Id
        self.name = name
        self.description = description
        self.user_id = user_id
        self.upload_date = upload_date
