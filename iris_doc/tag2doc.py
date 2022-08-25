import re
from typing import Dict, List, Tuple
from fs.base import FS
from enum import IntEnum

from iris_doc.language_specification import CommentSource, ErrorType, LanguageFormat


class Tag2Doc:

    __format: LanguageFormat
    __commentSources: Dict[str, CommentSource]

    def __init__(self, format: LanguageFormat, commentSources: Dict[str, CommentSource]) -> None:
        self.__format = format
        self.__commentSources = commentSources

    def __printf(self, error_type: ErrorType, key, comment_source: CommentSource = None):
        if error_type == ErrorType.FileNotFoundError:
            print('[{}] not found\n'.format(key))
        elif error_type == ErrorType.NotDeserializedError:
            print('[{}] parse error'.format(key))
            print('—— parameters contains empty object: {}\n'.format(
                comment_source.parameters))

    def __generateIndent(self, indent: int):
        return ' ' * indent

    def __generateDescription(self, format: LanguageFormat, description: str, indent: str) -> str:
        outputLines: List[str] = []
        for line in description.split('\n'):
            ws = ' ' if line.strip() != "" else ''
            outputLines.append(f"{indent}{format.comment2}{ws}{line}")

        return '\n'.join(outputLines)

    def __generatePairContent(self, pair1: str, pair2: str, indent: str, seperator: str, content: str) -> str:
        if content == None or content == "":
            return ""

        output: str = ""
        if pair1 is not None and pair1 != '':
            output += f"{indent}{pair1}{seperator}"

        output += content

        if pair2 is not None and pair2 != '':
            output += f"{seperator}{indent}{pair2}"

        return output

    def __generateSummary(self, format: LanguageFormat, comment_source: CommentSource, indent: str) -> str:
        return self.__generatePairContent(
            format.summary1,
            format.summary2,
            "",
            "\n",
            comment_source.description)

    def __generateParam(self, format: LanguageFormat, comment_source: CommentSource, indent: str) -> str:
        if comment_source.parameters == None:
            return ""

        def generate(param: Tuple[str, str]) -> str:
            out: str = self.__generatePairContent(
                format.param1,
                format.param2,
                "",
                "",
                param[0])

            out = self.__generatePairContent(
                out,
                format.param3,
                "",
                "",
                param[1])

            return out

        try:
            outList: List[str] = []
            for parameter in comment_source.parameters:
                for key in parameter:
                    outList.append(generate((key, parameter[key])))

            return '\n'.join(outList)

        except:
            self.__printf(ErrorType.NotDeserializedError,
                          comment_source.id, comment_source)
            return ''

    def __generateReturn(self, format: LanguageFormat, comment_source: CommentSource, indent: str) -> str:
        if comment_source.returns == '':
            return ''

        return self.__generatePairContent(
            format.return1,
            format.return2,
            "",
            "\n",
            comment_source.returns)

    def _generateComment(self, format: LanguageFormat, comment_source: CommentSource = None, indent: int = 2) -> str:
        str_indent = self.__generateIndent(indent)

        if comment_source == None or comment_source.is_hide:
            return self.__generatePairContent(
                format.comment1,
                format.comment3,
                str_indent,
                "\n",
                self.__generateDescription(format, format.ignore, str_indent))

        out: str = ""
        out += self.__generateSummary(format, comment_source, str_indent)

        # Only the type with "api", or not the parent object
        if comment_source.type_ == 'api' or len(comment_source.id.split("_")) > 2:
            if paramStr := self.__generateParam(format, comment_source, str_indent):
                out += "\n\n"
                out += paramStr

        if returnStr := self.__generateReturn(format, comment_source, str_indent):
            out += "\n\n"
            out += returnStr

        if out == "":
            return self.__generatePairContent(
                format.comment1,
                format.comment3,
                str_indent,
                "\n",
                self.__generateDescription(format, format.ignore, str_indent))

        return self.__generatePairContent(
            format.comment1,
            format.comment3,
            str_indent,
            "\n",
            self.__generateDescription(format, out, str_indent))

    def __getCommentSource(self, tag: str) -> CommentSource:
        if tag in self.__commentSources.keys():
            return self.__commentSources[tag]

        tagSpilt = tag.split('_')
        # The length of the tag spilt should be 3 for the member variable or enum value
        if len(tagSpilt) < 3:
            return None

        parentTag = f"{tagSpilt[0]}_{tagSpilt[1]}"
        if parentTag in self.__commentSources.keys():
            parentCommentSource = self.__commentSources[parentTag]
            for param in parentCommentSource.parameters:
                for pk in param:
                    if pk.lower() == tagSpilt[2].lower():
                        return CommentSource(id=tag,
                                             description=param[pk],
                                             is_hide=parentCommentSource.is_hide)

        return None

    def process(self, code: str) -> str:
        codeInLines = code.split('\n')
        outputLines: List[str] = []
        for line in codeInLines:
            m = re.match(r'\/\*\s(.*)\s\*\/', line.strip())
            if m:
                tag = m.group(1)
                comment_source: CommentSource = self.__getCommentSource(tag)

                if comment_source:
                    indent = line.find('/')
                    comment = self._generateComment(
                        self.__format, comment_source, indent)
                    outputLines.append(comment)
                    continue
                else:
                    self.__printf(ErrorType.FileNotFoundError, tag)

            outputLines.append(line)

        return '\n'.join(outputLines)
