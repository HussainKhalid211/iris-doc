from abc import ABC, abstractclassmethod
import os
import re
from typing import List
from fs.base import FS

from iris_doc.export_file_parser import ExportFileParser


class ExportFileParserCSharp(ExportFileParser):

    __fileSystem: FS

    def __init__(self, fileSystem: FS):
        self.__fileSystem = fileSystem

    def parseExportFiles(self, exportFilePath: str) -> List[str]:
        export_file_dir = exportFilePath
        files: List[str] = []

        file_list = self.__fileSystem.listdir(export_file_dir)
        for file in file_list:
            if file.endswith(".cs"):
                files.append(os.path.join(export_file_dir, file))

        type_dir = os.path.join(export_file_dir, "Types")
        file_list = self.__fileSystem.listdir(type_dir)
        for file in file_list:
            if file.endswith(".cs"):
                files.append(os.path.join(type_dir, file))

        files.append(os.path.join(export_file_dir, "VideoRender/VideoSurface.cs"))
        files.append(os.path.join(export_file_dir, "VideoRender/VideoSurfaceYUV.cs"))

        print(files)
        return files
