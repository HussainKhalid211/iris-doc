from abc import ABC, abstractmethod
from typing import Any


class PostPhase(ABC):

    @abstractmethod
    def run(self) -> Any:
        pass


class DefaultPostPhase(PostPhase):

    def run(self) -> Any:
        return
