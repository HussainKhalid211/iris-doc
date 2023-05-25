
import re
from abc import ABC, abstractmethod
from typing import List, Tuple, Callable, Optional

from fs.base import FS

TYPE_CLASS = "class"
TYPE_API = "api"
TYPE_CONSTRUCT = "construct"
TYPE_ENUM = "enum"
TYPE_EXTENSION = "extension"
TYPE_CONSTANT = "constant"


class LanguageSyntaxMatcher(ABC):

    def matchTag(self, line: str) -> str:
        """
        Return a matched tag
        """
        m = re.match(r'\/\*\s(.*)\s\*\/', line.strip())
        if m:
            return m.group(1)
        return None

    @abstractmethod
    def matchComment(self, line: str) -> str:
        """
        Return a matched comments or None
        """
        pass

    @abstractmethod
    def matchClass(self, line: str) -> str:
        """
        Return a matched class name or None
        """
        pass

    @abstractmethod
    def matchClassScopeStart(self, line: str) -> bool:
        """
        Whether match the class scope start
        """
        pass

    @abstractmethod
    def matchClassScopeEnd(self, line: str) -> bool:
        """
        Whether match the class scope end
        """
        pass

    @abstractmethod
    def matchClassConstructor(self, line: str, className: str) -> str:
        """
        Return a matched constructor of class or None
        """
        pass

    @abstractmethod
    def matchMemberFunction(self, line: str) -> str:
        """
        Return a matched member function of class or None
        """
        pass

    @abstractmethod
    def matchMemberVariable(self, line: str) -> str:
        """
        Return a matched member variable of class or None
        """
        pass

    @abstractmethod
    def matchEnum(self, line: str) -> str:
        """
        Return a matched enum name or None
        """
        pass

    def matchEnumScopeStart(self, line: str) -> bool:
        """
        Whether match the enum scope start
        """
        return self.matchClassScopeStart(line)

    def matchEnumScopeEnd(self, line: str) -> bool:
        """
        Whether match the enum scope end
        """
        return self.matchClassScopeEnd(line)

    @abstractmethod
    def matchEnumValue(self, line: str) -> str:
        """
        Return a matched enum value name or None
        """
        pass

    @abstractmethod
    def matchAnnotation(self, line: str) -> str:
        """
        Return a matched annotation name or None
        """
        pass

    @abstractmethod
    def matchExtension(self, line: str) -> str:
        """
        Return a matched extension name or None
        """
        pass

    def matchMemberVariableScopeStart(self, line: str) -> bool:
        return self.matchMemberVariable(line) is not None

    def matchMemberVariableScopeEnd(self, line: str) -> bool:
        return self.matchMemberVariable(line) is not None

    def matchExtensionScopeStart(self, line: str) -> bool:
        """
        Whether match the extension scope start
        """
        return self.matchClassScopeStart(line)

    def matchExtensionScopeEnd(self, line: str) -> bool:
        """
        Whether match the extension scope end
        """
        return self.matchExtensionScopeEnd(line)

    @abstractmethod
    def matchConstant(self, line: str) -> str:
        """
        Return a matched constant name or None
        """
        pass

    @abstractmethod
    def matchFunction(self, line: str) -> str:
        """
        Return a matched top-level function or None
        """
        pass

    def matchFunctionScopeStart(self, line: str) -> bool:
        """
        Whether match the function scope start
        """
        return self.matchClassScopeStart(line)

    def matchFunctionScopeEnd(self, line: str) -> bool:
        """
        Whether match the function scope end
        """
        return self.matchClassScopeEnd(line)

    def matchAbstractFunctionScopeEnd(self, line: str) -> bool:
        """
        Whether match the abstract function scope end, default just match if end with `;` 
        for most languages
        """
        return line.strip().endswith(";")

    def matchFunctionParameterScopeStart(self, functionName: str, line: str) -> bool:
        """
        Whether match the function parameter scope start
        """
        return self.matchMemberFunction(line) == functionName

    def matchFunctionParameterScopeEnd(self, line: str) -> bool:
        """
        Whether match the function parameter scope end
        """
        return ")" in line

    @abstractmethod
    def findFunctionParameterList(self, function_name: str, lines: List[str]) -> List[str]:
        """
        Find the function parameters as List
        """
        pass

    def findFunctionLink(self, class_name: str, line: str) -> str:
        """
        Get the link to an API method, given the class name and method line (flattened)
        """
        pass

    def findFunctionNameFromBlock(self, block: str, current_name: Optional[str]) -> str:
        """
        Find the function name from the function definition block (start from `matchFunctionScopeStart`, 
        and end with `matchFunctionScopeEnd` or `matchAbstractFunctionScopeEnd`). 

        The function name is returned by the `matchFunction` by default, if you want to fine-grained 
        to find out what the function name is from the block, you can override this function to resolve it.
        """
        return None


class Token:
    _offset: int
    _type: str
    _name1: str
    _name2: str
    _annotations: List[str]

    def __init__(self,
                 offset: int,
                 type: str,
                 name1: str,
                 name2: str = None,
                 annotations: List[str] = []):
        self._offset = offset
        self._type = type
        self._name1 = name1
        self._name2 = name2
        self._annotations = annotations

    def getOffset(self) -> int:
        # We want to add the tag above the annotations
        if len(self._annotations):
            return self._offset - len(self._annotations)

        return self._offset

    def _buildTag(self, type: str, name1: str, name2: str):
        tag = "{}_{}".format(type, name1)
        if name2 is not None:
            tag = "{}_{}".format(tag, name2)

        return "/* {} */".format(tag).lower()

    def toString(self):
        return self._buildTag(type=self._type, name1=self._name1, name2=self._name2)


class LineScanner(ABC):

    def _createToken(self,
                     offset: int,
                     type: str,
                     name1: str,
                     name2: str = None,
                     annotations: List[str] = []) -> Token:
        return Token(offset=offset, type=type, name1=name1, name2=name2, annotations=annotations)

    @abstractmethod
    def tokenize(self) -> List[Token]:
        """
        Tokenize the code by line, and return the tokenized collection.
        """
        pass


class DefaultLineScanner(LineScanner):
    __syntaxMatcher: LanguageSyntaxMatcher

    __fileLines: List[str] = []

    def __init__(self, syntaxMatcher: LanguageSyntaxMatcher, fileLines: List[str]) -> None:
        self.__syntaxMatcher = syntaxMatcher
        self.__fileLines = fileLines

    def _findMatchingIndex(self, lines: List[str], startIndex, method: Callable[[str], bool]):
        """
        Iterate through lines until we find a line where method returns true.
        """
        i = startIndex
        while (i < len(lines)):
            if method(lines[i].strip()):
                return i
            i += 1
        return -1

    def _findExtensionScopeStartIndex(self, lines: List[str], startIndex: int) -> int:
        i = startIndex
        while(i < len(lines)):
            if self.__syntaxMatcher.matchExtensionScopeStart(lines[i]):
                return i
            i += 1
        return -1

    def _findClassScopeStartIndex(self, lines: List[str], startIndex: int) -> int:
        return self._findMatchingIndex(lines, startIndex, self.__syntaxMatcher.matchClassScopeStart)

    def _findExtensionScopeStartIndex(self, lines: List[str], startIndex: int) -> int:
        return self._findMatchingIndex(lines, startIndex, self.__syntaxMatcher.matchExtensionScopeStart)

    def _findClassScopeEndIndex(self, lines: List[str], scopeStartIndex: int) -> int:
        if not self.__syntaxMatcher.matchClassScopeStart(lines[scopeStartIndex]) and \
            self.__syntaxMatcher.matchExtensionsScopeStart(lines[scopeStartIndex]):
            raise IndexError("The ExtensionsScopeStart is not correct.\n{lines[scopeStartIndex]}")

        scopeStack = []
        scopeStack.append(scopeStartIndex)

        i = scopeStartIndex + 1

        while (i < len(lines)):
            line = lines[i].strip()
            if self.__syntaxMatcher.matchFunctionScopeStart(line) or self.__syntaxMatcher.matchClassScopeStart(line):
                scopeStack.append(i)
            if self.__syntaxMatcher.matchClassScopeEnd(line) or self.__syntaxMatcher.matchFunctionScopeEnd(line):
                scopeStack.pop()
            if len(scopeStack) == 0:
                return i
            i += 1

        return -1

    def _findFunctionScopeStartIndex(self, lines: List[str], startIndex: int) -> int:
        return self._findMatchingIndex(lines, startIndex, self.__syntaxMatcher.matchFunctionScopeStart)

    def _findFunctionScopeEndIndex(self, lines: List[str], scopeStartIndex: int) -> int:
        scopeStack = []
        line = lines[scopeStartIndex].strip()
        # For a single line function, return the `scopeStartIndex` directly
        if self.__syntaxMatcher.matchFunctionScopeEnd(line) or \
                self.__syntaxMatcher.matchAbstractFunctionScopeEnd(line):
            return scopeStartIndex

        # If the first line not `matchFunctionScopeStart`, it should be a abstract function,
        # find the abstract function scope end directly for this case.
        if not self.__syntaxMatcher.matchFunctionScopeStart(line):
            i = scopeStartIndex
            while (i < len(lines)):
                line = lines[i].strip()
                if self.__syntaxMatcher.matchAbstractFunctionScopeEnd(line):
                    return i

                i += 1

            return -1

        scopeStack.append(scopeStartIndex)

        i = scopeStartIndex + 1

        while (i < len(lines)):
            line = lines[i].strip()
            if self.__syntaxMatcher.matchFunctionScopeEnd(line):
                scopeStack.pop()
            elif self.__syntaxMatcher.matchFunctionScopeStart(line):
                scopeStack.append(i)

            if len(scopeStack) == 0:
                return i

            i += 1

        return -1

    def _findFunctionParameterScopeEnd(self, functionName: str, lines: List[str], scopeStartIndex: int) -> int:
        if not self.__syntaxMatcher.matchFunctionParameterScopeStart(functionName, lines[scopeStartIndex]):
            raise IndexError("The FunctionParameterScopeStart is not correct.\n{lines[scopeStartIndex]}")
        return self._findMatchingIndex(lines, scopeStartIndex, self.__syntaxMatcher.matchFunctionParameterScopeEnd)

    def _findEnumScopeStartIndex(self, lines: List[str], startIndex: int) -> int:
        return self._findMatchingIndex(lines, startIndex, self.__syntaxMatcher.matchEnumScopeStart)

    def _findEnumScopeEndIndex(self, lines: List[str], scopeStartIndex: int) -> int:
        if not self.__syntaxMatcher.matchEnumScopeStart(lines[scopeStartIndex]):
            raise IndexError("The EnumScopeStart is not correct.\n{lines[scopeStartIndex]}")
        return self._findMatchingIndex(lines, scopeStartIndex + 1, self.__syntaxMatcher.matchEnumScopeEnd)

    def _getAnnotations(self, lineIndex: int) -> List[str]:
        annotations: List[str] = []
        index = lineIndex - 1
        if self.__syntaxMatcher.matchAnnotation(self.__fileLines[index]):
            while (index >= 0):
                if annotation := self.__syntaxMatcher.matchAnnotation(self.__fileLines[index]):
                    annotations.append(annotation)
                else:
                    break
                index -= 1
        return annotations

    def _getClassTokens(self, className: str, lineIndex: int, type: str = TYPE_CLASS) -> Tuple[int, List[Token]]:
        tokens: List[Token] = []
        classScopeStartIndex = self._findClassScopeStartIndex(
            self.__fileLines, lineIndex)
        if classScopeStartIndex == -1:
            classScopeStartIndex = self._findExtensionScopeStartIndex(
                self.__fileLines, lineIndex)
        classScopeEndIndex = self._findClassScopeEndIndex(
            self.__fileLines, classScopeStartIndex)
        tokens.append(self._createToken(
            offset=lineIndex,
            type=type,
            name1=className,
            annotations=self._getAnnotations(lineIndex)))
        i = classScopeStartIndex + 1
        while (i < classScopeEndIndex):
            line = self.__fileLines[i]
            ctName = self.__syntaxMatcher.matchClassConstructor(
                line, className)
            if ctName:
                tokens.append(self._createToken(
                    offset=i,
                    type=TYPE_CONSTRUCT,
                    name1=className,
                    name2=ctName,
                    annotations=self._getAnnotations(i)))
            # Match member variable
            elif self.__syntaxMatcher.matchMemberVariableScopeStart(line):
                # Some Objective C properties are across multiple lines, for example
                # @property (assign, nonatomic)
                #    NSInteger elapsedTime NS_SWIFT_NAME(elapsedTime);
                end_line = self._findMatchingIndex(self.__fileLines, i, self.__syntaxMatcher.matchMemberVariableScopeEnd)
                mvName = self.__syntaxMatcher.matchMemberVariable(' '.join(self.__fileLines[i:end_line+1]))
                # On some languages(e.g., dart) the member variable with Function type can lead to the
                # declaration to be formatted to multiple lines, such like:
                # ```
                #   final void Function(
                #       RtcConnection connection,
                #       int remoteUid,
                #       RemoteVideoState state,
                #       RemoteVideoStateReason reason,
                #       int elapsed)? onRemoteVideoStateChanged;
                # ```
                # so we need to find upon current line to get the correct insert index
                j = i
                while j - 1 >= classScopeStartIndex + 1 and self.__fileLines[j - 1].strip() != "" and \
                    not self.__syntaxMatcher.matchMemberVariableScopeStart(self.__fileLines[j - 1].strip()) and \
                    not self.__syntaxMatcher.matchMemberVariableScopeEnd(self.__fileLines[j - 1].strip()) and \
                        not self.__syntaxMatcher.matchAnnotation(self.__fileLines[j - 1].strip()):
                    j -= 1
                tokens.append(self._createToken(
                    offset=j,
                    type=TYPE_CLASS,
                    name1=className,
                    name2=mvName,
                    annotations=self._getAnnotations(j)))
                i = end_line

            # Match member function
            elif mfName := self.__syntaxMatcher.matchMemberFunction(line):
                functionTokens = self._getFunctionTokens(
                    className=className,
                    functionName=mfName,
                    lineIndex=i,
                    classScopeStartIndex=classScopeStartIndex,
                    classScopeEndIndex=classScopeEndIndex)

                tokens.extend(functionTokens[1])
                i = functionTokens[0] + 1
                continue
            i += 1
        return (classScopeEndIndex, tokens)

    def _findMatchingBounds(
            self,
            function_name: str,
            start_end: Tuple[int, int],
            match_start: Callable[[str, str], bool],
            match_end: Callable[[str], bool]
    ) -> Tuple[int, int]:
        index = start_end[0]
        found_start = False
        bounds_start_index = index
        bounds_end_index = start_end[1]
        while index < start_end[1]:
            line = self.__fileLines[index]

            if not found_start and match_start(function_name, line):
                bounds_start_index = index
                found_start = True
            if match_end(line):
                # Because the while loop will never read the last line, this if statement will often not fire.
                bounds_end_index = index
                break

            index += 1
        return [bounds_start_index, bounds_end_index]

    def _getFunctionParameterList(self,
                                  functionName: str,
                                  startIndex: int,
                                  endIndex: int) -> Tuple[List[str], int, int]:
        parameterList: List[str] = []
        [parameterScopeStartIndex, parameterScopeEndIndex] = self._findMatchingBounds(
            functionName, [startIndex, endIndex],
            self.__syntaxMatcher.matchFunctionParameterScopeStart, self.__syntaxMatcher.matchFunctionParameterScopeEnd
        )

        parameterList = self.__syntaxMatcher.findFunctionParameterList(
            functionName, self.__fileLines[parameterScopeStartIndex:parameterScopeEndIndex + 1])

        return (parameterList, parameterScopeStartIndex, parameterScopeEndIndex)

    def _getFunctionTokens(self,
                           className: str,
                           functionName: str,
                           lineIndex: int,
                           classScopeStartIndex: int,
                           classScopeEndIndex: int) -> Tuple[int, List[Token]]:
        tokens: List[Token] = []

        # function1##param1#param2#param3
        functionSignature = functionName

        functionScopeStartIndex = self._findFunctionScopeStartIndex(
            self.__fileLines, lineIndex)

        parameter_list_start_index = lineIndex
        parameter_list_end_index = classScopeEndIndex if functionScopeStartIndex == - \
            1 else functionScopeStartIndex

        parameterList, parameter_scope_start, parameter_scope_end = self._getFunctionParameterList(
            functionName=functionName,
            startIndex=parameter_list_start_index,
            endIndex=parameter_list_end_index)

        scope_end_index = parameter_scope_end

        actual_function_scope_start_index = functionScopeStartIndex if functionScopeStartIndex != -1 else lineIndex
        actual_function_scope_end_index = parameter_scope_end

        if functionScopeStartIndex != -1 and functionScopeStartIndex > classScopeStartIndex and functionScopeStartIndex < classScopeEndIndex:
            actual_function_scope_end_index = self._findFunctionScopeEndIndex(
                self.__fileLines, functionScopeStartIndex)
            scope_end_index = actual_function_scope_end_index
        elif actual_function_scope_start_index > classScopeStartIndex and actual_function_scope_start_index < classScopeEndIndex:
            actual_function_scope_end_index = self._findFunctionScopeEndIndex(
                self.__fileLines, actual_function_scope_start_index)
            scope_end_index = actual_function_scope_end_index

        block = "\n".join(
            self.__fileLines[actual_function_scope_start_index:actual_function_scope_end_index + 1])
        fine_grained_func_name = self.__syntaxMatcher.findFunctionNameFromBlock(block, functionName)
        functionSignature = fine_grained_func_name if fine_grained_func_name else functionSignature

        if len(parameterList) > 0:
            functionSignature = f'{functionSignature}##{"#".join(parameterList)}'

        token: Token
        if className:
            token = self._createToken(
                offset=lineIndex,
                type=TYPE_API,
                name1=className,
                name2=functionSignature,
                annotations=self._getAnnotations(lineIndex))
        else:
            token = self._createToken(
                offset=lineIndex, type=TYPE_API, name1=fine_grained_func_name if fine_grained_func_name else functionName,
                annotations=self._getAnnotations(lineIndex)
            )

        tokens.append(token)

        return scope_end_index, tokens

    def _getEnumTokens(self, enumName: str, lineIndex: int) -> Tuple[int, List[Token]]:
        tokens: List[Token] = []

        tokens.append(self._createToken(
            offset=lineIndex,
            type=TYPE_ENUM,
            name1=enumName,
            annotations=self._getAnnotations(lineIndex)))

        enumScopeStartIndex = self._findEnumScopeStartIndex(
            self.__fileLines, lineIndex)
        enumScopeEndIndex = self._findEnumScopeEndIndex(
            self.__fileLines, enumScopeStartIndex)

        i = enumScopeStartIndex + 1
        while (i < enumScopeEndIndex):
            line = self.__fileLines[i]

            enumValueName = self.__syntaxMatcher.matchEnumValue(line)
            if enumValueName:
                tokens.append(self._createToken(
                    offset=i,
                    type=TYPE_ENUM,
                    name1=enumName,
                    name2=enumValueName,
                    annotations=self._getAnnotations(i)))

            i += 1

        return (enumScopeEndIndex, tokens)

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        lineIndex: int = 0
        while (lineIndex < len(self.__fileLines)):
            fileLine = self.__fileLines[lineIndex]
            # Match class
            className = self.__syntaxMatcher.matchClass(fileLine)
            if className:
                classTokens = self._getClassTokens(
                    className=className, lineIndex=lineIndex)
                tokens.extend(classTokens[1])
                lineIndex = classTokens[0] + 1
                continue

            # Match enum
            enumName = self.__syntaxMatcher.matchEnum(fileLine)
            if enumName:
                enumTokens = self._getEnumTokens(
                    enumName=enumName, lineIndex=lineIndex)
                tokens.extend(enumTokens[1])

                lineIndex = enumTokens[0] + 1
                continue

            # Match extension
            extensionName = self.__syntaxMatcher.matchExtension(fileLine)
            if extensionName:
                extensionTokens = self._getClassTokens(
                    className=extensionName, lineIndex=lineIndex, type=TYPE_EXTENSION)
                tokens.extend(extensionTokens[1])
                lineIndex = extensionTokens[0] + 1
                continue

            # Match top-level function
            tfName = self.__syntaxMatcher.matchFunction(fileLine)
            if tfName:
                functionTokens = self._getFunctionTokens(
                    className=className,
                    functionName=tfName,
                    lineIndex=lineIndex,
                    classScopeStartIndex=-1,
                    classScopeEndIndex=len(self.__fileLines))
                tokens.extend(functionTokens[1])
                lineIndex = functionTokens[0] + 1
                continue

            # Match top-level const
            consName = self.__syntaxMatcher.matchConstant(fileLine)
            if consName:
                tokens.append(self._createToken(
                    offset=lineIndex,
                    type=TYPE_CONSTANT,
                    name1=consName,
                    annotations=self._getAnnotations(lineIndex)))

            lineIndex += 1

        return tokens


class TagBuilder:

    __syntaxMatcher: LanguageSyntaxMatcher

    def __init__(self, syntaxMatcher: LanguageSyntaxMatcher):
        self.__syntaxMatcher = syntaxMatcher

    def _createLineScanner(self, syntaxMatcher: LanguageSyntaxMatcher, fileLines: List[str]) -> LineScanner:
        return DefaultLineScanner(syntaxMatcher, fileLines=fileLines)

    def build(self, sourceFileLines: List[str]) -> List[str]:
        outputFiles: List[str] = []
        fileLines: List[str] = []

        for line in sourceFileLines:
            if self.__syntaxMatcher.matchComment(line) or self.__syntaxMatcher.matchTag(line):
                continue
            fileLines.append(line)

        scanner = self._createLineScanner(
            self.__syntaxMatcher, fileLines)
        tokens = scanner.tokenize()

        index = 0
        startIndex = 0
        while (index < len(tokens)):
            token = tokens[index]

            offset = token.getOffset()
            outputFiles.extend(fileLines[startIndex:offset])
            tag = token.toString()
            if tag:
                outputFiles.append(tag)

            outputFiles.append(fileLines[offset])
            index += 1
            startIndex = offset + 1

        if startIndex < len(fileLines):
            outputFiles.extend(
                fileLines[startIndex:len(fileLines)])

        return outputFiles


class ApiTagger:

    _fileSystem: FS

    _tagBuilder: TagBuilder

    def __init__(self, fileSystem: FS, tagBuilder: TagBuilder):
        self._fileSystem = fileSystem
        self._tagBuilder = tagBuilder

    def process(self, filePath: str) -> None:
        file = self._fileSystem.open(filePath)

        outputFileLines = self._tagBuilder.build(
            str(file.read()).splitlines())
        file = self._fileSystem.open(filePath, mode="w")
        file.write('\n'.join(outputFileLines))
        file.flush()
        file.close()
