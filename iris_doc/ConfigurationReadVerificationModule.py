import json
import os
from typing import List, Tuple
from fs.base import FS
import yaml

from iris_doc.language_specification import ErrorType, LanguageFormat


class ConfigurationReadVerificationModule:
    __fmt = LanguageFormat()
    __fileSystem: FS

    def __init__(self, fileSystem: FS) -> None:
        self.__fileSystem = fileSystem

    def set_config(self, config_path: str) -> ErrorType:
        if not isinstance(config_path, str):
            return ErrorType.TypeError

        actual_path: str
        if os.path.isabs(config_path):
            actual_path = config_path
        else:
            actual_path = os.path.join(os.getcwd(), config_path)

        with self.__fileSystem.open(os.path.abspath(actual_path)) as file:
            configDict = yaml.safe_load(file)

            self.__fmt = LanguageFormat.from_yaml(configDict)

        return ErrorType.Ok

    def get_fmt(self) -> Tuple[ErrorType, LanguageFormat]:
        if self.__fmt.comment1:
            return ErrorType.Ok, self.__fmt
        else:
            return ErrorType.ConfigNotSetError, self.__fmt
