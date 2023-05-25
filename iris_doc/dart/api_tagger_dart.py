from iris_doc.api_tagger import TYPE_API, TYPE_CLASS, TYPE_CONSTRUCT, TYPE_EXTENSION, LanguageSyntaxMatcher, Token, LineScanner, DefaultLineScanner, TagBuilder
from typing import List, Tuple
import re


class DartSyntaxMatcher(LanguageSyntaxMatcher):
    def matchComment(self, line: str) -> str:
        if line.strip().startswith("///"):
            return line

        return None

    def matchClass(self, line: str) -> str:
        m = re.match(
            r'(abstract )?class ([A-Za-z\<\>0-9_]+)(.*){?$', line.strip(), re.M | re.I)
        if m:
            return m.group(2)

        return None

    def matchClassConstructor(self, line: str, className: str) -> str:
        # const constructor
        m = re.match(
            r'(const )?' + className + r'\(\{?', line.strip(), re.M | re.I)
        if m:
            return className

        # non-const constructor
        m = re.match(
            r'(const )?' + className + r'\.([A-Za-z\<\>0-9_]+)\((.*)?', line.strip(), re.M | re.I)
        if m:
            return m.group(2)

        # factory constructor with .
        m = re.match(
            r'factory ' + className + r'\.([A-Za-z\<\>0-9_]+)\((.*)?', line.strip(), re.M | re.I)
        if m:
            return m.group(1)

        # factory constructor
        m = re.match(
            r'factory ' + className + r'\((.*)?', line.strip(), re.M | re.I)
        if m:
            return className

        return None

    def matchMemberFunction(self, line: str) -> str:
        if line.strip().startswith("final"):
            return None

        m = re.match(
            r'(static )?([A-Za-z0-9_]+)\<?(.*)?\>? ([A-Za-z0-9_]+)\((.*)(\)?( {)?|;?)$', line.strip(), re.M | re.I)
        if m:
            return m.group(4)

        m = re.match(
            r'(static )?([A-Za-z0-9_]+)\<?(.*)?\>? ([A-Za-z0-9_]+)\((.*)\)\=\>(.*)', line.strip(), re.M | re.I)
        if m:
            return m.group(4)

        return None

    def matchMemberVariable(self, line: str) -> str:
        # final int? ipListSize;
        m = re.match(
            r'final (.*) ([A-Za-z0-9_]+);', line.strip(), re.M | re.I)
        if m:
            return m.group(2)

        m = re.match(r'([A-Za-z0-9_]+);$', line.strip())
        if m:
            return m.group(1)

        m = re.match(r'(.*) ([A-Za-z0-9_]+);$', line.strip())
        if m:
            return m.group(2)

        return None

    def matchEnum(self, line: str) -> str:
        m = re.match(r'enum (.*) {', line.strip(), re.M | re.I)
        if m:
            return m.group(1)

        return None

    def matchEnumValue(self, line: str) -> str:
        m = re.match(r'([A-Za-z0-9_]+),?$', line.strip(), re.M | re.I)
        if m:
            return m.group(1)

        return None

    def matchAnnotation(self, line: str) -> str:
        m = re.match(r'^@(.*)', line.strip())
        if m:
            return m.group(1)

        return None

    def matchExtension(self, line: str) -> str:
        m = re.match(
            r'extension (.*) on (.*) {', line.strip(), re.M | re.I)
        if m:
            return m.group(1)
        return None

    def matchConstant(self, line: str) -> str:
        m = re.match(
            r'const ([A-Za-z\<\>0-9_]*) ([A-Za-z0-9_]+) = (.*);', line.strip(), re.M | re.I)
        if m:
            return m.group(2)

        m = re.match(
            r'const ([A-Za-z0-9_]+) = (.*);', line.strip(), re.M | re.I)
        if m:
            return m.group(1)

        return None

    def matchFunction(self, line: str) -> str:
        return self.matchMemberFunction(line)

    def matchClassScopeStart(self, line: str) -> bool:
        return line.strip().endswith("{")

    def matchClassScopeEnd(self, line: str) -> bool:
        return line.strip().startswith("}")

    def findFunctionParameterList(self, function_name: str, lines: List[str]) -> List[str]:
        single_line = "".join(map(
            lambda x: x.strip(), lines
        ))
        parameterList: List[str] = []
        m = re.match(
            r'(.*)' + function_name + r'\(\ ?\{?([0-9a-zA-Z,=<>.?()\s]*)\}?\)(.*)', single_line)
        if m:
            parameterBlock = m.group(2).lstrip('{').rstrip('}')
            parameterBlockSplit = parameterBlock.split(',')
            for parameter in parameterBlockSplit:
                # Split default value =
                # e.g., MediaSourceType type = MediaSourceType.primaryCameraSource
                if "=" in parameter:
                    p = parameter.split(' = ')[0].split(' ')[-1]
                    if p:
                        parameterList.append(p)
                else:
                    p = parameter.split(' ')[-1]
                    if p:
                        parameterList.append(p)

        return parameterList

class DartToken(Token):

    __buildInAnnotations: List[str] = [
        "private", "protected", "override", "internal"]

    def toString(self):
        type = self._type

        if next((x for x in self._annotations if x in self.__buildInAnnotations), None):
            return None

        if type == TYPE_EXTENSION:
            return "/// @nodoc"

        # Force mark the function/member generated by json_serializable/terra to @nodoc
        # TODO(littlegnal): Decouple this from the tag, maybe it's better to move to tag2doc.py
        if type == TYPE_CONSTRUCT:
            if self._name2.lower() == "fromjson":
                return "/// @nodoc"
        if type == TYPE_API:
            if (self._name2 and self._name2.lower() == "tojson") or \
                    self._name1.lower().endswith("ext") and (self._name2.lower() == "value" or self._name2.lower() == "fromvalue"):
                return "/// @nodoc"

        return super()._buildTag(type=type, name1=self._name1, name2=self._name2)


class DartLineScanner(DefaultLineScanner):
    def _createToken(self,
                     offset: int,
                     type: str,
                     name1: str,
                     name2: str = None,
                     annotations: List[str] = []) -> Token:
        return DartToken(offset, type, name1, name2, annotations)


class DartTagBuilder(TagBuilder):
    def __init__(self):
        super().__init__(DartSyntaxMatcher())

    def _createLineScanner(self, syntaxMatcher: LanguageSyntaxMatcher, fileLines: List[str]) -> LineScanner:
        return DartLineScanner(syntaxMatcher, fileLines)
