from typing import Dict
import unittest
from iris_doc.dart.api_tagger_dart import DartTagBuilder
from iris_doc.language_specification import CommentSource, LanguageFormat
from iris_doc.tag2doc import Tag2Doc


class CommentGroup(unittest.TestCase):

    def test_comment2Only(self):
        format: LanguageFormat = LanguageFormat(
            comment1="",
            comment2="///",
            comment3="",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="*[",
            param2="] ",
            param3="",
            return1="### Return",
            return2="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="field1",
            description="This is a class field",
            parameters=[{"param1": "param value"}],
            returns="This is return",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)
        expectedResult = """
  /// This is a class field
  ///
  /// *[param1] param value
  ///
  /// ### Return
  /// This is return
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))

    def test_comment1_comment2(self):
        format: LanguageFormat = LanguageFormat(
            comment1="///",
            comment2="///",
            comment3="",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="*[",
            param2="] ",
            param3="",
            return1="### Return",
            return2="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="field1",
            description="This is a class field",
            parameters=[{"param1": "param value"}],
            returns="This is return",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)

        expectedResult = """
  ///
  /// This is a class field
  ///
  /// *[param1] param value
  ///
  /// ### Return
  /// This is return
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))

    def test_comment1_comment2_comment3(self):
        format: LanguageFormat = LanguageFormat(
            comment1="///",
            comment2="///",
            comment3="///",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="*[",
            param2="] ",
            param3="",
            return1="### Return",
            return2="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="field1",
            description="This is a class field",
            parameters=[{"param1": "param value"}],
            returns="This is return",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)

        expectedResult = """
  ///
  /// This is a class field
  ///
  /// *[param1] param value
  ///
  /// ### Return
  /// This is return
  ///
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))


class SummaryGroup(unittest.TestCase):

    def test_summary1(self):
        format: LanguageFormat = LanguageFormat(
            comment1="",
            comment2="///",
            comment3="",
            summary1="<summary>",
            summary2="",
            tag1="",
            tag2="",
            param1="*[",
            param2="] ",
            param3="",
            return1="### Return",
            return2="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="field1",
            description="This is a class field",
            parameters=[{"param1": "param value"}],
            returns="This is return",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)
        expectedResult = """
  /// <summary>
  /// This is a class field
  ///
  /// *[param1] param value
  ///
  /// ### Return
  /// This is return
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))

    def test_summary1_summary2(self):
        format: LanguageFormat = LanguageFormat(
            comment1="",
            comment2="///",
            comment3="",
            summary1="<summary>",
            summary2="</summary>",
            tag1="",
            tag2="",
            param1="*[",
            param2="] ",
            param3="",
            return1="### Return",
            return2="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="field1",
            description="This is a class field",
            parameters=[{"param1": "param value"}],
            returns="This is return",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)

        expectedResult = """
  /// <summary>
  /// This is a class field
  /// </summary>
  ///
  /// *[param1] param value
  ///
  /// ### Return
  /// This is return
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))


class ParamGroup(unittest.TestCase):

    def test_param1(self):
        format: LanguageFormat = LanguageFormat(
            comment1="",
            comment2="///",
            comment3="",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="<param name=\"",
            param2="",
            param3="",
            return1="### Return",
            return2="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="field1",
            description="This is a class field",
            parameters=[{"param1": "param value"}],
            returns="This is return",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)
        expectedResult = """
  /// This is a class field
  ///
  /// <param name="param1param value
  ///
  /// ### Return
  /// This is return
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))

    def test_param1_param2(self):
        format: LanguageFormat = LanguageFormat(
            comment1="",
            comment2="///",
            comment3="",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="<param name=\"",
            param2="\"> ",
            param3="",
            return1="### Return",
            return2="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="field1",
            description="This is a class field",
            parameters=[{"param1": "param value"}],
            returns="This is return",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)

        expectedResult = """
  /// This is a class field
  ///
  /// <param name="param1"> param value
  ///
  /// ### Return
  /// This is return
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))

    def test_param1_param2_param3(self):
        format: LanguageFormat = LanguageFormat(
            comment1="",
            comment2="///",
            comment3="",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="<param name=\"",
            param2="\">",
            param3="</param>",
            return1="### Return",
            return2="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="field1",
            description="This is a class field",
            parameters=[{"param1": "param value"}],
            returns="This is return",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)

        expectedResult = """
  /// This is a class field
  ///
  /// <param name="param1">param value</param>
  ///
  /// ### Return
  /// This is return
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))


class ReturnGroup(unittest.TestCase):

    def test_return1(self):
        format: LanguageFormat = LanguageFormat(
            comment1="",
            comment2="///",
            comment3="",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="*[",
            param2="] ",
            param3="",
            return1="<returns>",
            return2="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="field1",
            description="This is a class field",
            parameters=[{"param1": "param value"}],
            returns="This is return",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)
        expectedResult = """
  /// This is a class field
  ///
  /// *[param1] param value
  ///
  /// <returns>
  /// This is return
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))

    def test_return1_return2(self):
        format: LanguageFormat = LanguageFormat(
            comment1="",
            comment2="///",
            comment3="",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="*[",
            param2="] ",
            param3="",
            return1="<returns>",
            return2="</returns>",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="field1",
            description="This is a class field",
            parameters=[{"param1": "param value"}],
            returns="This is return",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)
        expectedResult = """
  /// This is a class field
  ///
  /// *[param1] param value
  ///
  /// <returns>
  /// This is return
  /// </returns>
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))


class GenerateCommentSmokeTest(unittest.TestCase):
    def test_hasParamNoReturn(self):
        format: LanguageFormat = LanguageFormat(
            comment1="",
            comment2="///",
            comment3="",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="*[",
            param2="] ",
            param3="",
            return1="<returns>",
            return2="</returns>",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="api",
            id="api_imediaplayer_adjustpublishsignalvolume",
            name="adjustPublishSignalVolume",
            description="Adjusts the volume of the media file for publishing.\nAfter connected to the Agora server, you can call this method to adjust the volume of the media file heard by the remote user.",
            parameters=[
                {"volume": "The volume, which ranges from 0 to 400:\n 0: Mute.\n 100: (Default) The original volume.\n 400: Four times the original volume (amplifying the audio signals by four times).\n "}],
            returns="",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)
        expectedResult = """
  /// Adjusts the volume of the media file for publishing.
  /// After connected to the Agora server, you can call this method to adjust the volume of the media file heard by the remote user.
  ///
  /// *[volume] The volume, which ranges from 0 to 400:
  ///  0: Mute.
  ///  100: (Default) The original volume.
  ///  400: Four times the original volume (amplifying the audio signals by four times).
  /// """
        self.assertEquals(result, expectedResult.lstrip('\n'))

    def test_noParamHasReturn(self):
        format: LanguageFormat = LanguageFormat(
            comment1="",
            comment2="///",
            comment3="",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="*[",
            param2="] ",
            param3="",
            return1="<returns>",
            return2="</returns>",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="field1",
            description="This is a class field",
            parameters=[],
            returns="This is return",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)

        expectedResult = """
  /// This is a class field
  ///
  /// <returns>
  /// This is return
  /// </returns>
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))

    def test_isHide(self):
        format: LanguageFormat = LanguageFormat(
            comment1="",
            comment2="///",
            comment3="",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="*[",
            param2="] ",
            param3="",
            return1="<returns>",
            return2="</returns>",
            link1="",
            link2="",
            ignore="@nodoc")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="field1",
            description="This is a class field",
            parameters=[],
            returns="This is return",
            deprecated="",
            note="",
            warning="",
            is_hide=True)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)

        expectedResult = """
  /// @nodoc
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))

    def test_badCommentSource(self):
        format: LanguageFormat = LanguageFormat(
            comment1="",
            comment2="///",
            comment3="",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="*[",
            param2="] ",
            param3="",
            return1="<returns>",
            return2="</returns>",
            link1="",
            link2="",
            ignore="@nodoc")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="",
            description="",
            parameters=[],
            returns="",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_one_field1": commentSource}
        result = Tag2Doc(format, commentSources)._generateComment(
            format, commentSource)

        expectedResult = """
  /// @nodoc
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))


class Tag2DocTest(unittest.TestCase):
    def test_addCommentToCode(self):
        format: LanguageFormat = LanguageFormat(
            comment1="",
            comment2="///",
            comment3="",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="*[",
            param2="] ",
            param3="",
            return1="",
            return2="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="api",
            id="api_imediaplayer_adjustpublishsignalvolume",
            name="adjustPublishSignalVolume",
            description="Adjusts the volume of the media file for publishing.\nAfter connected to the Agora server, you can call this method to adjust the volume of the media file heard by the remote user.",
            parameters=[
                {"volume": "The volume, which ranges from 0 to 400:\n 0: Mute.\n 100: (Default) The original volume.\n 400: Four times the original volume (amplifying the audio signals by four times)."}],
            returns="",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "api_imediaplayer_adjustpublishsignalvolume": commentSource}
        code = """
  /* api_imediaplayer_adjustpublishsignalvolume */
  Future<void> adjustPublishSignalVolume(int volume);
"""
        result = Tag2Doc(format, commentSources).process(
            code.rstrip().lstrip('\n'))
        expectedResult = """
  /// Adjusts the volume of the media file for publishing.
  /// After connected to the Agora server, you can call this method to adjust the volume of the media file heard by the remote user.
  ///
  /// *[volume] The volume, which ranges from 0 to 400:
  ///  0: Mute.
  ///  100: (Default) The original volume.
  ///  400: Four times the original volume (amplifying the audio signals by four times).
  Future<void> adjustPublishSignalVolume(int volume);
"""
        self.assertEquals(result, expectedResult.rstrip().lstrip('\n'))


if __name__ == '__main__':
    unittest.main()
