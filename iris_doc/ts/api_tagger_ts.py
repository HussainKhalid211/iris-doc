from iris_doc.api_tagger import LanguageSyntaxMatcher, Token, LineScanner, DefaultLineScanner, TagBuilder
from typing import List, Tuple
import re


class TSSyntaxMatcher(LanguageSyntaxMatcher):
    def matchComment(self, line: str) -> str:
        if line.strip().startswith("/*") or line.strip().startswith("*") or line.strip().startswith("*/"):
            return line

        return None

    def matchClass(self, line: str) -> str:
        m = re.match(
            r'(export )?(abstract )?(class|interface) ([A-Za-z<>0-9_]+)(.*){?$', line.strip())
        if m:
            return m.group(4)

        return None

    def matchClassConstructor(self, line: str, className: str) -> str:
        return None

    def matchMemberFunction(self, line: str) -> str:
        m = re.match(
            r'(abstract |get |set |public |private )([A-Za-z0-9_]+)\((.*)(\)?( {)?|;?)$', line.strip())
        if m:
            return m.group(2)
        m = re.search(
            r'([A-Za-z0-9_]+)\??\((.*)(\)?( {)?|;?)$', line.strip())
        if m:
            return m.group(1)

        return None

    def matchMemberVariable(self, line: str) -> str:
        m = re.match(r'([A-Za-z0-9_]+)(\?)?: (.*);', line.strip())
        if m:
            return m.group(1)

        return None

    def matchEnum(self, line: str) -> str:
        m = re.match(r'export enum (.*) {', line.strip(), re.M | re.I)
        if m:
            return m.group(1)

        return None

    def matchEnumValue(self, line: str) -> str:
        m = re.match(r'([A-Za-z0-9_]+) = (.*),?$', line.strip())
        if m:
            return m.group(1)

        return None

    def matchAnnotation(self, line: str) -> str:
        m = re.match(r'^@(.*)', line.strip())
        if m:
            return m.group(1)

        return None

    def matchExtension(self, line: str) -> str:
        return None

    def matchConstant(self, line: str) -> str:
        m = re.match(
            r'export const (.*)(: )?(.*) = (.*)', line.strip(), re.M | re.I)
        if m:
            return m.group(1)

        return None

    def matchFunction(self, line: str) -> str:
        m = re.match(
            r'(export )?function ([A-Za-z0-9_]+)\((.*)(\)?( {)?|;?)$', line.strip(), re.M | re.I)
        if m:
            return m.group(2)

        return None

    def matchClassScopeStart(self, line: str) -> bool:
        return line.strip().endswith("{") and not line.strip().startswith("}")

    def matchClassScopeEnd(self, line: str) -> bool:
        return line.strip().startswith("}") and not line.strip().endswith("{")

    def findFunctionParameterList(self, function_name: str, lines: List[str]) -> List[str]:
        single_line = " ".join(map(
            lambda x: x.strip(), lines
        ))
        parameterList: List[str] = []
        m = re.match(
            r'(.*)' + function_name + r'\??\((.*)\)(.*)', single_line)
        if m:
            parameterBlock = m.group(2)
            parameterBlockSplit = parameterBlock.split(',')
            for parameter in parameterBlockSplit:
                # Split default value =
                # e.g., MediaSourceType type = MediaSourceType.primaryCameraSource
                if "=" in parameter:
                    parameterList.append(parameter.split(' = ')[0].split(' ')[-1])
                else:
                    m = re.match(r'\s?([A-Za-z0-9_]+)\??: (.*)', parameter)
                    if m:
                        parameterList.append(m.group(1))

        return parameterList


# class DartToken(Token):
#     def toString(self):
#         type = self._type
#         if type == "extension":
#             type = "class"

#         return super()._buildTag(type=type, name1=self._name1, name2=self._name2)


# class DartLineScanner(DefaultLineScanner):
#     def _createToken(self,
#                      offset: int,
#                      type: str,
#                      name1: str,
#                      name2: str = None,
#                      annotations: List[str] = []) -> Token:
#         return DartToken(offset, type, name1, name2, annotations)


class TSTagBuilder(TagBuilder):
    def __init__(self):
        super().__init__(TSSyntaxMatcher())

    # def _createLineScanner(self, syntaxMatcher: LanguageSyntaxMatcher, fileLines: List[str]) -> LineScanner:
    #     return DartLineScanner(syntaxMatcher, fileLines)
