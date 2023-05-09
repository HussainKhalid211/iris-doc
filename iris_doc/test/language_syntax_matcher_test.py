from typing import List
import fs.memoryfs
import unittest
from iris_doc.api_tagger import ApiTagger, LanguageSyntaxMatcher, LineScanner, TagBuilder
from iris_doc.dart.api_tagger_dart import DartLineScanner, DartSyntaxMatcher, DartTagBuilder


class FakeSyntaxMatcher(DartSyntaxMatcher):
    """
    Extends the `DartSyntaxMatcher` to reuse most logic
    """

    function_blocks: List[str]

    def __init__(self) -> None:
        self.function_blocks = []

    def findFunctionNameFromBlock(self, block: str) -> str:
        self.function_blocks.append(block)
        return "FixedFakeFuncName"


class FakeTagBuilder(TagBuilder):
    fake_syntax_matcher: FakeSyntaxMatcher

    def __init__(self):
        self.fake_syntax_matcher = FakeSyntaxMatcher()
        super().__init__(self.fake_syntax_matcher)

    def _createLineScanner(self, syntaxMatcher: LanguageSyntaxMatcher, fileLines: List[str]) -> LineScanner:
        return DartLineScanner(syntaxMatcher, fileLines)


class TestApiTaggerDart(unittest.TestCase):

    __fileSystem: fs.memoryfs.MemoryFS
    __apiTagger: ApiTagger
    __fake_tag_builder: FakeTagBuilder

    @classmethod
    def setUpClass(self):
        self.__fileSystem = fs.memoryfs.MemoryFS()
        self.__fake_tag_builder = FakeTagBuilder()
        self.__apiTagger = ApiTagger(
            self.__fileSystem, self.__fake_tag_builder)

    @classmethod
    def tearDownClass(self):
        self.__fileSystem.close()

    def test_findFunctionNameFromBlock(self):
        path = "member_function.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
class MemberFunction {
    Map<String, dynamic> toJson() => _$DirectCdnStreamingMediaOptionsToJson(this);

    Map<String, dynamic> soLoooooooooooongFunction() => 
        _$DirectCdnStreamingMediaOptionsToJson(this);

    Future<void> setVideoEncoderConfiguration(VideoEncoderConfiguration config);

    Future<void> setBeautyEffectOptions(
      {required bool enabled,
      required BeautyOptions options,
      MediaSourceType type = MediaSourceType.primaryCameraSource});

    Future<void> setExternalVideoSource(
      {required bool enabled,
      required bool useTexture,
      ExternalVideoSourceType sourceType = ExternalVideoSourceType.videoFrame,
      SenderOptions encodedVideoOption = const SenderOptions()});
}
        """)

        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_memberfunction */
class MemberFunction {
/* api_memberfunction_fixedfakefuncname */
    Map<String, dynamic> toJson() => _$DirectCdnStreamingMediaOptionsToJson(this);

/* api_memberfunction_fixedfakefuncname */
    Map<String, dynamic> soLoooooooooooongFunction() => 
        _$DirectCdnStreamingMediaOptionsToJson(this);

/* api_memberfunction_fixedfakefuncname##config */
    Future<void> setVideoEncoderConfiguration(VideoEncoderConfiguration config);

/* api_memberfunction_fixedfakefuncname##enabled#options#type */
    Future<void> setBeautyEffectOptions(
      {required bool enabled,
      required BeautyOptions options,
      MediaSourceType type = MediaSourceType.primaryCameraSource});

/* api_memberfunction_fixedfakefuncname##enabled#usetexture#sourcetype#encodedvideooption */
    Future<void> setExternalVideoSource(
      {required bool enabled,
      required bool useTexture,
      ExternalVideoSourceType sourceType = ExternalVideoSourceType.videoFrame,
      SenderOptions encodedVideoOption = const SenderOptions()});
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

        self.assertEqual(self.__fake_tag_builder.fake_syntax_matcher.function_blocks[0], """
    Map<String, dynamic> toJson() => _$DirectCdnStreamingMediaOptionsToJson(this);
""".strip("\n"))

        self.assertEqual(self.__fake_tag_builder.fake_syntax_matcher.function_blocks[1], """
    Map<String, dynamic> soLoooooooooooongFunction() => 
        _$DirectCdnStreamingMediaOptionsToJson(this);
""".strip("\n"))

        self.assertEqual(self.__fake_tag_builder.fake_syntax_matcher.function_blocks[2], """
    Future<void> setVideoEncoderConfiguration(VideoEncoderConfiguration config);
""".strip("\n"))

        self.assertEqual(self.__fake_tag_builder.fake_syntax_matcher.function_blocks[3], """
    Future<void> setBeautyEffectOptions(
      {required bool enabled,
      required BeautyOptions options,
      MediaSourceType type = MediaSourceType.primaryCameraSource});
""".strip("\n"))

        self.assertEqual(self.__fake_tag_builder.fake_syntax_matcher.function_blocks[4], """
    Future<void> setExternalVideoSource(
      {required bool enabled,
      required bool useTexture,
      ExternalVideoSourceType sourceType = ExternalVideoSourceType.videoFrame,
      SenderOptions encodedVideoOption = const SenderOptions()});
""".strip("\n"))
