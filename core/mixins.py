import json
from datetime import datetime
from uuid import UUID


class SerializeMixin:

    @property
    def serialize(self):
        data = self.__dict__
        if data.get("_state"):
            data.pop("_state")
        return SerializeMixin._serialize(data)

    @staticmethod
    def _serialize(data):
        if isinstance(data, (str, list)):
            return data

        for key, value in data.items():

            if isinstance(value, dict):
                data[key] = SerializeMixin._serialize(value)
            if isinstance(value, (datetime, UUID)):
                data[key] = value.__str__()
        return data
