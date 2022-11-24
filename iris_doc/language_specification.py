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
    __fileSystem: FS
    __config: LanguageSpecificationConfig
    __commentSources: Dict[str, CommentSource] = {}
    __templateFilePaths: List[str] = []

    def __init__(self, fileSystem: FS, config: LanguageSpecificationConfig) -> None:
        self.__fileSystem = fileSystem
        self.__config = config
        self.__commentSources.clear()
        self.__templateFilePaths.clear()

    def addTemplateFilePath(self, path: str):
        self.__templateFilePaths.append(path)

    def setLanguageSpecificationConfig(self, config: LanguageSpecificationConfig):
        self.__config = config

    def specialize(self) -> bool:
        pass

    def __parseJson(self, jsonContent: str):
        elementsCopy = json.loads(jsonContent)
        for element in json.loads(jsonContent):
            id_: str = element['id']

            name_: str = element['name'].lower()

            tmpSource = CommentSource.from_json(json.dumps(element))

            if tmpSource.is_hide is not True and name_.endswith(']') and name_.find("[") != -1:
                name_ = name_[:name_.index("[")].rstrip()

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

            element['type_'] = new_id[: new_id.find('_')]

            if element['type_'] == "api":
                tmpCS: CommentSource = CommentSource.from_json(json.dumps(element))
                if len(tmpCS.parameters) > 0:
                    parameterNames: List[str] = []
                    for parameters in tmpCS.parameters:
                        for pk in parameters.keys():
                            parameterNames.append(pk)
                    new_id = f'{new_id}##{"#".join(parameterNames).lower()}'

            element['id'] = new_id

            if element['id'] in self.__commentSources:
                continue

            finalCommentSource: CommentSource = CommentSource.from_json(
                json.dumps(element))
            parent_parameters = finalCommentSource.parameters

            if (element['type_'] == "class" or element['type_'] == "enum") and len(parent_parameters) > 0:
                finalCommentSource.parameters = []
                self.__commentSources[element['id']] = finalCommentSource

                for parameters in parent_parameters:
                    for parameterk in parameters:
                        parameterId = f'{finalCommentSource.id}_{parameterk.lower()}'
                        self.__commentSources[parameterId] = CommentSource(
                            id=parameterId,
                            name=parameterk,
                            description=parameters[parameterk],
                            is_hide=finalCommentSource.is_hide)
            else:
                self.__commentSources[element['id']] = finalCommentSource

    def deserialize(self) -> ErrorType:
        for path in self.__templateFilePaths:
            with self.__fileSystem.open(path, 'r') as file:
                jsonContent = file.read()
                self.__parseJson(jsonContent)

        return ErrorType.Ok

    def getAllCommentSources(self) -> Dict[str, CommentSource]:
        return self.__commentSources
