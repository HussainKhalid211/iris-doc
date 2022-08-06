from abc import ABC, abstractmethod
from typing import List


class ExportFileParser(ABC):

    @abstractmethod
    def parseExportFiles(self, exportFilePath: str) -> List[str]:
        pass

class DefaultExportFileParser(ExportFileParser):

    def parseExportFiles(self, exportFilePath: str) -> List[str]:
        return []