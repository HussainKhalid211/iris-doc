import unittest
from typing import Dict

from iris_doc.language_specification import CommentSource, LanguageFormat
from iris_doc.tag2doc import Tag2Doc


class CommentGroup(unittest.TestCase):

    def test_commentWithEmptyParameters(self):
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
            return3="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_one_field1",
            name="field1",
            description="This is a class field",
            parameters=[{}, None, {"param1": "param value"}],
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

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
            return3="",
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

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
            return3="",
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

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
            return3="",
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))


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
            return3="",
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

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
            return3="",
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))


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
            return3="",
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

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
            return3="",
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

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
            return3="",
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))


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
            return3="",
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

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
            return2="",
            return3="</returns>",
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))


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
            return2="",
            return3="</returns>",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="api",
            id="api_imediaplayer_adjustpublishsignalvolume",
            name="adjustPublishSignalVolume",
            description="Adjusts the volume of the media file for publishing.\nAfter connected to the Agora server, you can call this method to adjust the volume of the media file heard by the remote user.",
            parameters=[
                {
                    "volume": "The volume, which ranges from 0 to 400:\n 0: Mute.\n 100: (Default) The original volume.\n 400: Four times the original volume (amplifying the audio signals by four times).\n "}],
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
        self.assertEqual(result, expectedResult.lstrip('\n'))

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
            return2="",
            return3="</returns>",
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

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
            return2="",
            return3="</returns>",
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

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
            return2="",
            return3="</returns>",
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))


class Tag2DocTest(unittest.TestCase):

    def test_apiNotFoundSourceWithSameParam(self):
        format: LanguageFormat = LanguageFormat(
            comment1="/**",
            comment2=" *",
            comment3=" */",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="",
            param2="",
            param3="",
            return1="",
            return2="",
            return3="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="api",
            id="api_irtcengine_setvideoencoderconfiguration",
            name="setVideoEncoderConfiguration",
            description="Sets the video encoder configuration.\nSets the encoder configuration for the local video.You can call this method either before or after joining a channel. If the user does not need to reset the video encoding properties after joining the channel, Agora recommends calling this method before enableVideo to reduce the time to render the first video frame.",
            parameters=[
                {
                    "config": "Video profile. See VideoEncoderConfiguration ."}],
            returns="0: Success.< 0: Failure.",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "api_irtcengine_setvideoencoderconfiguration##config": commentSource,
        }
        code = """
    /* api_imediarecorder_startrecording##config */
    abstract startRecording(config: MediaRecorderConfiguration): number;
    """
        result = Tag2Doc(format, commentSources).process(
            code.rstrip().lstrip('\n'))

        expectedResult = """
    /* api_imediarecorder_startrecording##config */
    abstract startRecording(config: MediaRecorderConfiguration): number;
    """
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

    def test_classWithUnderscore(self):
        format: LanguageFormat = LanguageFormat(
            comment1="/**",
            comment2=" *",
            comment3=" */",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="",
            param2="",
            param3="",
            return1="",
            return2="",
            return3="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_virtual_background_source",
            name="VIRTUAL_BACKGROUND_SOURCE",
            description="The custom background image.\n",
            parameters=[],
            returns="",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSourceParam = CommentSource(
            id="class_virtual_background_source_blur_degree",
            name="BLUR_DEGREE",
            description="The degree of blurring applied to the custom background image. This parameter takes effect only when the type of the custom background image is BackgroundBlur.",
            returns="",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_virtual_background_source": commentSource,
            "class_virtual_background_source_blur_degree": commentSourceParam,
        }
        code = """
      /* class_virtual_background_source */
      export class VIRTUAL_BACKGROUND_SOURCE {
        /* class_virtual_background_source_blur_degree */
        BLUR_DEGREE?: BackgroundBlurDegree;
      }
    """
        result = Tag2Doc(format, commentSources).process(
            code.rstrip().lstrip('\n'))

        expectedResult = """
      /**
       * The custom background image.
       *
       */
      export class VIRTUAL_BACKGROUND_SOURCE {
        /**
         * The degree of blurring applied to the custom background image. This parameter takes effect only when the type of the custom background image is BackgroundBlur.
         */
        BLUR_DEGREE?: BackgroundBlurDegree;
      }
    """
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

    def test_paramWithoutUnderscore(self):
        format: LanguageFormat = LanguageFormat(
            comment1="/**",
            comment2=" *",
            comment3=" */",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="",
            param2="",
            param3="",
            return1="",
            return2="",
            return3="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_virtualbackgroundsource",
            name="VirtualBackgroundSource",
            description="The custom background image.\n",
            parameters=[],
            returns="",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSourceBlurDegree = CommentSource(
            id="class_virtualbackgroundsource_blurdegree",
            name="blurDegree",
            description="The degree of blurring applied to the custom background image. This parameter takes effect only when the type of the custom background image is BackgroundBlur.",
            returns="",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_virtualbackgroundsource": commentSource,
            "class_virtualbackgroundsource_blurdegree": commentSourceBlurDegree,
        }
        code = """
  /* class_virtualbackgroundsource */
  export class VirtualBackgroundSource {
    /* class_virtualbackgroundsource_blurdegree */
    blurDegree?: BackgroundBlurDegree;
  }
"""
        result = Tag2Doc(format, commentSources).process(
            code.rstrip().lstrip('\n'))
        expectedResult = """
  /**
   * The custom background image.
   *
   */
  export class VirtualBackgroundSource {
    /**
     * The degree of blurring applied to the custom background image. This parameter takes effect only when the type of the custom background image is BackgroundBlur.
     */
    blurDegree?: BackgroundBlurDegree;
  }
"""
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

    def test_paramWithUnderscore(self):
        format: LanguageFormat = LanguageFormat(
            comment1="/**",
            comment2=" *",
            comment3=" */",
            summary1="",
            summary2="",
            tag1="",
            tag2="",
            param1="",
            param2="",
            param3="",
            return1="",
            return2="",
            return3="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="class",
            id="class_virtualbackgroundsource",
            name="VirtualBackgroundSource",
            description="The custom background image.\n",
            parameters=[],
            returns="",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSourceParam = CommentSource(
            id="class_virtualbackgroundsource_blur_degree",
            name="blur_degree",
            description="The degree of blurring applied to the custom background image. This parameter takes effect only when the type of the custom background image is BackgroundBlur.",
            returns="",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "class_virtualbackgroundsource": commentSource,
            "class_virtualbackgroundsource_blur_degree": commentSourceParam,
        }
        code = """
  /* class_virtualbackgroundsource */
  export class VirtualBackgroundSource {
    /* class_virtualbackgroundsource_blur_degree */
    blur_degree?: BackgroundBlurDegree;
  }
"""
        result = Tag2Doc(format, commentSources).process(
            code.rstrip().lstrip('\n'))

        expectedResult = """
  /**
   * The custom background image.
   *
   */
  export class VirtualBackgroundSource {
    /**
     * The degree of blurring applied to the custom background image. This parameter takes effect only when the type of the custom background image is BackgroundBlur.
     */
    blur_degree?: BackgroundBlurDegree;
  }
"""
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

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
            return3="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="api",
            id="api_imediaplayer_adjustpublishsignalvolume##volume",
            name="adjustPublishSignalVolume",
            description="Adjusts the volume of the media file for publishing.\nAfter connected to the Agora server, you can call this method to adjust the volume of the media file heard by the remote user.",
            parameters=[
                {
                    "volume": "The volume, which ranges from 0 to 400:\n 0: Mute.\n 100: (Default) The original volume.\n 400: Four times the original volume (amplifying the audio signals by four times)."}],
            returns="",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "api_imediaplayer_adjustpublishsignalvolume##volume": commentSource}
        code = """
  /* api_imediaplayer_adjustpublishsignalvolume##volume */
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
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))

    def test_addCommentToTopLevelFuntion(self):
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
            return3="",
            link1="",
            link2="",
            ignore="")
        commentSource = CommentSource(
            type_="api",
            id="api_createagorartcengine",
            name="createAgoraRtcEngine",
            description="Adjusts the volume of the media file for publishing.\nAfter connected to the Agora server, you can call this method to adjust the volume of the media file heard by the remote user.",
            parameters=[
                {
                    "volume": "The volume, which ranges from 0 to 400:\n 0: Mute.\n 100: (Default) The original volume.\n 400: Four times the original volume (amplifying the audio signals by four times)."}],
            returns="",
            deprecated="",
            note="",
            warning="",
            is_hide=False)
        commentSources: Dict[str, CommentSource] = {
            "api_createagorartcengine": commentSource}
        code = """
  /* api_createagorartcengine */
  RtcEngine createAgoraRtcEngine();
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
  RtcEngine createAgoraRtcEngine();
"""
        self.assertEqual(result, expectedResult.rstrip().lstrip('\n'))


if __name__ == '__main__':
    unittest.main()
