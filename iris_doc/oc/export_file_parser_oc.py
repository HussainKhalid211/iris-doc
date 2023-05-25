from abc import ABC, abstractclassmethod
import os
import re
from typing import List
from fs.base import FS

from iris_doc.export_file_parser import ExportFileParser


class ExportFileParserObjC(ExportFileParser):

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
                r'#import ["\<](.*\/)?(.*)["\>]\;?', line.strip(), re.I)
            if m:
                p = m.group(2)
                files.append(os.path.join(exportFileDir, p))
        print(files)
        self.fixStarComments(files)
        return files
    
    lines = []

    def fixStarComments(self, file_paths):
        """
        Fixes comment blocks, so that the middle lines are always prepended with "*".
        Args:
            file_paths (List[str]): A list of file paths to fix.
        Raises:
            FileNotFoundError: If a file path in file_paths does not exist.
        """
        for filename in file_paths:
            # read the file
            with open(filename, "r") as f:
                lines = str(f.read()).splitlines()

            self.fixCommentsOnLines(lines)
            # write the modified content back to the file
            with open(filename, "w") as f:
                f.write('\n'.join(lines))

    def fixCommentsOnLines(self, lines: List[str]):
        """
        Fixes comment blocks that start with "/**" or "/*" but do not end with "*/" on the same line in the given list of strings.
        Args:
            lines (List[str]): A list of strings representing lines of code.
            These lines are modified in-line
        """
        # define a regular expression to match strings that start with "/**" or "/*" and do not end with "*/" on the same line
        regex_comment_start = r"\s*//?\*\*?(?:(?!\*/).)*$"
        comment_middle = r"^\s*(/{2,3}|\*){1}(\s.*|$)$"
        comment_active = False
        # loop through each match
        for i, line in enumerate(lines):
            if comment_active:
                if '*/' in line:
                    comment_active = False
                elif re.match(comment_middle, line) is None:
                    lines[i] = " * " + lines[i]
                continue
            # check if the second line starts with "* "
            if re.match(regex_comment_start, line) is not None:
                comment_active = True
