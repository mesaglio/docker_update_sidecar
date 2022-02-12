"""Errors schemas"""
from dataclasses import asdict, dataclass


@dataclass
class AppError:
    """Application error object"""

    msg: str

    # def __post_init__(self) -> None:
    #    self.error = self.error.value  # type: ignore

    def json(self):
        """Serialize object as a JSON"""

        return asdict(self)


def app_error_dumper(obj: AppError):
    return obj.json()


class GenericException(Exception):
    """Generic"""
