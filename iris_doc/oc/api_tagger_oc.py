from iris_doc.api_tagger import TYPE_API, TYPE_CLASS, TYPE_CONSTRUCT, TYPE_EXTENSION, LanguageSyntaxMatcher, Token, LineScanner, DefaultLineScanner, TagBuilder
from typing import List, Optional
import re


class ObjCSyntaxMatcher(LanguageSyntaxMatcher):
    def matchComment(self, line: str) -> str:
        """
        Return a matched comments or None. Objective-C Comments start with /* or ///
        """
        if line.strip().startswith("/*") or line.strip().startswith("*") or line.strip().startswith("*/") or (line.strip().endswith("*/") and '/*' not in line.strip()) or line.strip().startswith("///"):
            return line
        return None

    def matchClass(self, line: str) -> str:
        m = re.match(r".*@(interface|protocol)\s+(\w+)\s*(:|\<|$)", line.strip())
        if m:
            return m.group(2)
        return None

    def matchClassConstructor(self, line: str, className: str) -> str:
        """
        Return a matched constructor of class or None
        """
        m = re.match(r"[-+]{1}\s*\(\s*instancetype\s*\)\s*" + className + r"\s*\w*\s*{?", line.strip())
        if m:
            return m.group(0)
        return None

    def matchMemberFunction(self, line: str) -> str:
        """
        Return a matched member function of class or None
        """
        m = re.match(r"[-+]\s*\((.*?)\)\s*(\w+.*?)\s*:?", line.strip())
        if m:
            return m.group(2)
        return None

    def matchMemberVariable(self, line: str) -> str:
        """
        Return a matched member variable of class or None
        """
        m = re.match(r'@property.*?\b(\w+)\b(?=\s*(?:NS_SWIFT_NAME|\;))', line.strip())
        if m:
            return m.group(1)
        return None

    def matchEnum(self, line: str) -> str:
        """
        Return a matched enum name or None
        """
        m = re.match(r".*typedef\s*NS_ENUM\s*\(.*\, (\w*)\)\ {?", line.strip())
        if m:
            return m.group(1)
        return None

    def matchEnumValue(self, line: str) -> str:
        """
        Return a matched enum value name or None
        """
        m = re.match(r"\s*(\w+)\s*=\s*[^,]+,?", line.strip())
        if m:
            return m.group(1)
        return None

    def matchAnnotation(self, line: str) -> str:
        """
        Return a matched annotation name or None
        """
        if 'NS_ASSUME_NONNULL' in line:
            return line
        m = re.match(r'^@\w+$', line.strip())
        if m:
            return line.strip()
        m = re.match(
            r'^\s*(?!.*(NS_ASSUME_NONNULL_BEGIN|NS_ASSUME_NONNULL_END|IBInspectable|IBOutlet|IBAction|\b(?:class|enum|interface|protocol|struct)\b))__(attribute|deprecated|availability)(__)?\b.*',
            line.strip()
        )
        if m:
            return m.group(1)
        return None

    def matchExtension(self, line: str) -> str:
        """
        Return a matched extension name or None
        """
        m = re.match(r"@interface\s+(\w+)\s*\(\s*(\w+)\s*\)", line.strip())
        if m:
            return m.group(1) + "(" + m.group(2) + ")"
        return None

    def matchConstant(self, line: str) -> str:
        m = re.match(r'static const ([A-Za-z\<\>0-9_]*) ([A-Za-z0-9_]+) = (.*);', line.strip(), re.M | re.I)
        if m:
            return m.group(2)

        m = re.match(r'static const ([A-Za-z0-9_]+) = (.*);', line.strip(), re.M | re.I)
        if m:
            return m.group(1)

        return None

    def matchFunction(self, line: str) -> str:
        return self.matchMemberFunction(line)

    def matchClassScopeStart(self, line: str) -> bool:
        # Define the regex to match the start of a Objective-C class definition
        # pattern = r'.*@interface\s+(\w+)\s*:'
        pattern = r'^.*@(interface|protocol)\s+(\w+)\s*(:|\<)'

        # Use the regex to search for a match in the line
        match = re.search(pattern, line)

        # Return True if a match was found, else return False
        return match is not None

    def matchClassScopeEnd(self, line: str) -> bool:
        return re.match(r'\s*@end\s*', line) is not None

    def matchExtensionsScopeStart(self, line: str) -> bool:
        return self.matchExtension(line) is not None


    def matchEnumScopeStart(self, line: str) -> bool:
        return self.matchEnum(line)

    def matchEnumScopeEnd(self, line: str) -> bool:
        return re.match(r'\s*};\s*', line) is not None

    def matchFunctionParameterScopeEnd(self, line: str) -> bool:
        return ';' in line

    def matchMemberVariableScopeStart(self, line: str) -> bool:
        return re.match(r'@property.*\b(\w+)\b', line.strip()) is not None

    def matchMemberVariableScopeEnd(self, line: str) -> bool:
        return ';' in line

    def findFunctionNameFromBlock(self, block: str, current_name: Optional[str]) -> str:
        if not current_name:
            current_name = self.matchMemberFunction(block)
        if current_name.lower() in ["rtcengine"]:
            return self.findCallbackName(current_name, block)
        return None

    def findCallbackName(self, function_name: str, line: str) -> str:
        pattern = r'([^:\n-+]*):'

        matches: List[str] = re.findall(pattern, line.split('NS_SWIFT_NAME')[0].strip())

        if len(matches) > 1:
            return matches[1]
        return function_name

    def findFunctionParameterList(self, function_name: str, lines: List[str]) -> List[str]:
        single_line = " ".join(map(
            lambda x: x.strip(), lines
        ))
        return re.findall(r':\s*\([\w+\s*\*?\s*_?\(\)^<>,\w+\s*]*\)(\w+)', single_line)

    def matchFunctionScopeStart(self, line: str) -> bool:
        return '{' in line

    def matchFunctionScopeEnd(self, line: str) -> bool:
        return '}' in line

    def findFunctionLink(self, class_name: str, line: str) -> str:
        pattern = r'([^:\n-+]*):'

        matches: List[str] = re.findall(pattern, line.split('NS_SWIFT_NAME')[0].strip())

        matches_joined = ':'.join(matches)
        return f'{class_name}/{matches_joined}'

class ObjCToken(Token):

    __buildInAnnotations: List[str] = [
        "private", "protected", "override", "internal"]

    def toString(self):
        type = self._type
        if next((x for x in self._annotations if x in self.__buildInAnnotations), None):
            return None

        # if type == TYPE_EXTENSION:
        #     self._name1 = self._name1.replace('(','').replace(')','')

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


class ObjCLineScanner(DefaultLineScanner):
    def _createToken(self,
                     offset: int,
                     type: str,
                     name1: str,
                     name2: str = None,
                     annotations: List[str] = []) -> Token:
        return ObjCToken(offset, type, name1, name2, annotations)

class ObjCTagBuilder(TagBuilder):
    def __init__(self):
        super().__init__(ObjCSyntaxMatcher())
    def _createLineScanner(self, syntaxMatcher: LanguageSyntaxMatcher, fileLines: List[str]) -> LineScanner:
        return ObjCLineScanner(syntaxMatcher, fileLines)
