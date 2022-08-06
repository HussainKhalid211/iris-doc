from abc import ABC, abstractclassmethod
import os
import re
from typing import List
from fs.base import FS

from iris_doc.export_file_parser import ExportFileParser


class ExportFileParserDart(ExportFileParser):

    __fileSystem: FS

    def __init__(self, fileSystem: FS):
        self.__fileSystem = fileSystem

    def parseExportFiles(self, exportFilePath: str) -> List[str]:
        exportFileDir = os.path.dirname(exportFilePath)

        files: List[str] = []
        exportFile = self.__fileSystem.open(exportFilePath)
        exportFileLines: List[str] = exportFile.readlines()
        for line in exportFileLines:
            m = re.match(
                r'export \'(.*)\'\;', line.strip(), re.I)
            if m:
                p = m.group(1)
                files.append(os.path.join(exportFileDir, p))

        return files
