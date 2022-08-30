from enum import IntEnum
import json
import re
from fs.base import FS
from typing import Dict, List, Tuple


class Structure:
    @classmethod
    def from_json(cls, data):
        return cls(**(json.loads(data)))

    @classmethod
    def from_yaml(cls, data):
        return cls(**data)


class ErrorType(IntEnum):
    Ok = 0
    TypeError = 1
    FileNotFoundError = 2
    FileNotReadError = 3
    NotDeserializedError = 4
    KeyError = 5
    ConfigNotSetError = 6


class CommentSource(Structure):
    def __init__(self, type_: str = None,
                 id: str = None,
                 name: str = None,
                 description: str = None,
                 parameters: List[Dict[str, str]] = None,
                 returns: str = None,
                 deprecated: str = None,
                 note: str = None,
                 warning: str = None,
                 is_hide: bool = None):
        self.type_ = type_
        self.id = id
        self.name = name
        self.description = description
        self.parameters = parameters
        self.returns = returns
        self.deprecated = deprecated
        self.note = note
        self.warning = warning
        self.is_hide = is_hide


class LanguageFormat(Structure):
    def __init__(self, comment1: str = None,
                 comment2: str = "///",
                 comment3: str = None,
                 summary1: str = None,
                 summary2: str = None,
                 tag1: str = None,
                 tag2: str = None,
                 param1: str = None,
                 param2: str = None,
                 param3: str = None,
                 return1: str = None,
                 return2: str = None,
                 link1: str = None,
                 link2: str = None,
                 ignore: str = None):
        self.comment1 = comment1
        self.comment2 = comment2
        self.comment3 = comment3
        self.summary1 = summary1
        self.summary2 = summary2
        self.tag1 = tag1
        self.tag2 = tag2
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.return1 = return1
        self.return2 = return2
        self.link1 = link1
        self.link2 = link2
        self.ignore = ignore


class LanguageSpecificationConfig:
    isCallback2class: bool
    isCallback2api: bool
    idPatternV2: bool

    def __init__(self, isCallback2class: bool, isCallback2api: bool, idPatternV2: bool) -> None:
        self.isCallback2class = isCallback2class
        self.isCallback2api = isCallback2api
        self.idPatternV2 = idPatternV2


class LanguageSpecificationModule:
    __template_doc = ''
    __fileSystem: FS
    __config: LanguageSpecificationConfig
    __commentSources: Dict[str, CommentSource] = {}

    def __init__(self, fileSystem: FS, config: LanguageSpecificationConfig) -> None:
        self.__fileSystem = fileSystem
        self.__config = config

    def read_template_file(self, path: str) -> ErrorType:
        if not isinstance(path, str):
            return ErrorType.TypeError

        try:
            file = self.__fileSystem.open(path)
            self.__template_doc = file.read()
            self.__template_doc = re.sub(' {3,}', '', self.__template_doc)
            file.close()
        except FileNotFoundError:
            return ErrorType.FileNotFoundError

        return ErrorType.Ok

    def setLanguageSpecificationConfig(self, config: LanguageSpecificationConfig):
        self.__config = config

    def specialize(self) -> bool:
        pass

    def deserialize(self) -> ErrorType:
        if self.__template_doc == '':
            return ErrorType.FileNotReadError

        elementsCopy = json.loads(self.__template_doc)
        for element in json.loads(self.__template_doc):
            id_ = element['id']
            name_ = element['name'].lower()

            if id_.endswith('_ng'):
                id_ = re.sub(r'_ng$', '', id_)

            id_split = id_.split('_')

            new_id = '_'.join(id_split)

            if self.__config.idPatternV2:
                new_id_split = new_id.split('_')

                newType = new_id_split[0]
                newName1 = new_id_split[1]

                tmpType = "class" if newType == "api" or newType == "callback" else newType

                parentElement = next(
                    (e for e in elementsCopy if e['id'] == f"{tmpType}_{newName1}"), None)
                if parentElement:
                    newName1 = parentElement['name'].lower()
                else:
                    newName1 = element['name'].lower()

                if self.__config.isCallback2api and newType == "callback":
                    newType = "api"

                if self.__config.isCallback2class and newType == "callback":
                    newType = "class"

                if len(new_id_split) == 3:
                    newName2 = name_
                    new_id = f"{newType}_{newName1}_{newName2}"
                else:
                    new_id = f"{newType}_{newName1}"

            element['id'] = new_id

            element['type_'] = new_id[: new_id.find('_')]

            self.__commentSources[element['id']] = CommentSource.from_json(
                json.dumps(element))

        return ErrorType.Ok

    def getAllCommentSources(self) -> Dict[str, CommentSource]:
        return self.__commentSources
