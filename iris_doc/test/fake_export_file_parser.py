from iris_doc.export_file_parser import ExportFileParser
from typing import List


class FakeExportFileParser(ExportFileParser):
    __returnPathList: List[str]

    def __init__(self, returnPathList: List[str]) -> None:
        self.__returnPathList = returnPathList

    def parseExportFiles(self, exportFilePath: str) -> List[str]:
        return self.__returnPathList
