import uuid
from rest_framework.exceptions import NotFound
from .constants import RESTAURANT_NOT_FOUND


class Validators:

    @staticmethod
    def validate_uuid(pk: str):
        """
            Checks if the provided pk is a valid uuid.
        """
        try:
            uuid.UUID(pk)
        except:
            raise NotFound(RESTAURANT_NOT_FOUND)