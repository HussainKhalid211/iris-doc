from abc import ABC, abstractclassmethod
import os
import re
from typing import List
from fs.base import FS

from iris_doc.export_file_parser import ExportFileParser


class ExportFileParserTS(ExportFileParser):

    __fileSystem: FS

    def __init__(self, fileSystem: FS):
        self.__fileSystem = fileSystem

    def parseExportFiles(self, exportFilePath: str) -> List[str]:
        exportFileDir = os.path.dirname(exportFilePath)

        files: List[str] = []
        # On TS, also add the index.ts file as the export file
        files.append(exportFilePath)
        exportFile = self.__fileSystem.open(exportFilePath)
        exportFileLines: List[str] = exportFile.readlines()
        for line in exportFileLines:
            m = re.match(
                r'export \* from \'\.\/(.*)\'\;', line.strip(), re.I)
            if m:
                p = m.group(1)
                if os.path.exists(os.path.join(exportFileDir, f'{p}.ts')):
                    files.append(os.path.join(exportFileDir, f'{p}.ts'))
                elif os.path.exists(os.path.join(exportFileDir, f'{p}.tsx')):
                    files.append(os.path.join(exportFileDir, f'{p}.tsx'))

        return files
