
from dataclasses import dataclass

@dataclass
class Container:
    def __init__(self, id, image, status, name):
        self.id = id
        self.image = image
        self.status = status
        self.name = name

    def __str__(self):
        return f"Container(id={self.id},name={self.name},status={self.status})"

    def __repr__(self):
        return self.__str__()
