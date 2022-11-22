from iris_doc.api_tagger import LanguageSyntaxMatcher, Token, LineScanner, DefaultLineScanner, TagBuilder
from typing import List, Tuple
import re


class CSharpSyntaxMatcher(LanguageSyntaxMatcher):
    def matchComment(self, line: str) -> str:
        if line.strip().startswith("///"):
            return line

        return None

    def matchClass(self, line: str) -> str:
        m = re.match(
            r'(public )?(abstract )?(class|interface) ([A-Za-z\<\>0-9_]+)(.*){?$', line.strip())
        if m:
            return m.group(4)

        return None

    def matchClassConstructor(self, line: str, className: str) -> str:
        return None

    def matchMemberFunction(self, line: str) -> str:
        m = re.match(
            r'^(public |protected |private )?(abstract |virtual |override )?([A-Za-z0-9_]+ )([A-Za-z0-9z]+)\(.*\)', line.strip())
        if m:
            return m.group(4)

        m = re.match(
            r'^(abstract |virtual |override )?(public |protected |private )?([A-Za-z0-9_]+)\s([A-Za-z0-9z]+)\(.*\)', line.strip())
        if m:
            return m.group(4)

        return None

    def matchMemberVariable(self, line: str) -> str:
        m = re.match(
            r'^(public |protected |private )?([A-Za-z0-9_<>]+ )([A-Za-z0-9_]+)(;| \{ set; get; \}|\s\=\s.*;)', line.strip())
        if m:
            return m.group(3)

        return None

    def matchEnum(self, line: str) -> str:
        m = re.match(r'public enum (.*)$', line.strip(), re.M | re.I)
        if m:
            return m.group(1)

        return None

    def matchEnumValue(self, line: str) -> str:
        m = re.match(r'([A-Za-z0-9_]+) = (.*),?$', line.strip())
        if m:
            return m.group(1)

        return None

    def matchAnnotation(self, line: str) -> str:
        m = re.match(r'^([.*])', line.strip())
        if m:
            return m.group(1)

        return None

    def matchExtension(self, line: str) -> str:
        return None

    def matchConstant(self, line: str) -> str:
        # m = re.match(
        #     r'(export )?const (.*)(\: )?(.*) = (.*)', line.strip(), re.M | re.I)
        # if m:
        #     return m.group(2)

        return None

    def matchFunction(self, line: str) -> str:
        # m = re.match(
        #     r'(export )?function ([A-Za-z0-9_]+)\((.*)(\)?( {)?|;?)$', line.strip(), re.M | re.I)
        # if m:
        #     return m.group(2)

        return None

    def matchClassScopeStart(self, line: str) -> bool:
        return line.strip().endswith("{")

    def matchClassScopeEnd(self, line: str) -> bool:
        return line.strip().startswith("}")


class CSharpTagBuilder(TagBuilder):
    def __init__(self):
        super().__init__(CSharpSyntaxMatcher())
