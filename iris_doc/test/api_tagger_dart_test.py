import fs.memoryfs
import unittest
from iris_doc.api_tagger import ApiTagger, TagBuilder
from iris_doc.dart.api_tagger_dart import DartTagBuilder


class TestApiTaggerDart(unittest.TestCase):

    __fileSystem: fs.memoryfs.MemoryFS
    __apiTagger: ApiTagger

    @classmethod
    def setUpClass(self):
        self.__fileSystem = fs.memoryfs.MemoryFS()
        self.__apiTagger = ApiTagger(
            self.__fileSystem, DartTagBuilder())

    @classmethod
    def tearDownClass(self):
        self.__fileSystem.close()

    def test_matchMemberFunction(self):
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
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_memberfunction */
class MemberFunction {
/// @nodoc
    Map<String, dynamic> toJson() => _$DirectCdnStreamingMediaOptionsToJson(this);

/* api_memberfunction_soloooooooooooongfunction */
    Map<String, dynamic> soLoooooooooooongFunction() => 
        _$DirectCdnStreamingMediaOptionsToJson(this);

/* api_memberfunction_setvideoencoderconfiguration */
    Future<void> setVideoEncoderConfiguration(VideoEncoderConfiguration config);

/* api_memberfunction_setbeautyeffectoptions */
    Future<void> setBeautyEffectOptions(
      {required bool enabled,
      required BeautyOptions options,
      MediaSourceType type = MediaSourceType.primaryCameraSource});
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchMemberFunctionWithBody(self):
        path = "member_function.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
class MemberFunction {
    Future<String?> getAssetAbsolutePath(String assetPath) async {
        final impl = this as RtcEngineImpl;
        final p = await impl.engineMethodChannel
            .invokeMethod<String>('getAssetAbsolutePath', assetPath);
        return p;
    }

    static Future<MediaPlayerController> create(
        {required RtcEngine rtcEngine,
        required VideoCanvas canvas,
        bool useFlutterTexture = false,
        bool useAndroidSurfaceView = false}) async {
        return MediaPlayerImpl.createMediaPlayerController(
            rtcEngine: rtcEngine,
            canvas: canvas,
            useFlutterTexture: useFlutterTexture,
            useAndroidSurfaceView: useAndroidSurfaceView);
    }
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_memberfunction */
class MemberFunction {
/* api_memberfunction_getassetabsolutepath */
    Future<String?> getAssetAbsolutePath(String assetPath) async {
        final impl = this as RtcEngineImpl;
        final p = await impl.engineMethodChannel
            .invokeMethod<String>('getAssetAbsolutePath', assetPath);
        return p;
    }

/* api_memberfunction_create */
    static Future<MediaPlayerController> create(
        {required RtcEngine rtcEngine,
        required VideoCanvas canvas,
        bool useFlutterTexture = false,
        bool useAndroidSurfaceView = false}) async {
        return MediaPlayerImpl.createMediaPlayerController(
            rtcEngine: rtcEngine,
            canvas: canvas,
            useFlutterTexture: useFlutterTexture,
            useAndroidSurfaceView: useAndroidSurfaceView);
    }
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchFunctionMemberVariable(self):
        path = "function_member_variable.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
class FunctionMemberVariable {
    final void Function(RtcConnection connection, int elapsed)?
        onJoinChannelSuccess;
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_functionmembervariable */
class FunctionMemberVariable {
/* class_functionmembervariable_onjoinchannelsuccess */
    final void Function(RtcConnection connection, int elapsed)?
        onJoinChannelSuccess;
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchFunctionMemberVariableWithSoManyLines(self):
        path = "function_member_variable.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
class FunctionMemberVariable {
  final void Function(
      RtcConnection connection,
      int remoteUid,
      RemoteVideoState state,
      RemoteVideoStateReason reason,
      int elapsed)? onRemoteVideoStateChanged;

  final void Function(
        RtcConnection connection, int width, int height, int elapsed)?
    onFirstLocalVideoFrame;
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_functionmembervariable */
class FunctionMemberVariable {
/* class_functionmembervariable_onremotevideostatechanged */
  final void Function(
      RtcConnection connection,
      int remoteUid,
      RemoteVideoState state,
      RemoteVideoStateReason reason,
      int elapsed)? onRemoteVideoStateChanged;

/* class_functionmembervariable_onfirstlocalvideoframe */
  final void Function(
        RtcConnection connection, int width, int height, int elapsed)?
    onFirstLocalVideoFrame;
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchFunctionMemberVariablesAndMemberFunctions(self):
        path = "function_member_variables_and_member_functions.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
class FunctionMemberVariable {
    final void Function(RtcConnection connection, int elapsed)?
        onJoinChannelSuccess;

    Future<void> memberFunction();
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_functionmembervariable */
class FunctionMemberVariable {
/* class_functionmembervariable_onjoinchannelsuccess */
    final void Function(RtcConnection connection, int elapsed)?
        onJoinChannelSuccess;

/* api_functionmembervariable_memberfunction */
    Future<void> memberFunction();
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchMultiFunctionMemberVariablesAndMemberFunctions(self):
        path = "function_member_variables_and_member_functions.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
class FunctionMemberVariable {
    final void Function(RtcConnection connection, int elapsed)?
        onJoinChannelSuccess;

    Future<void> memberFunction();
}

class FunctionMemberVariable2 {
    final void Function(RtcConnection connection, int elapsed)?
        onJoinChannelSuccess;

    Future<void> memberFunction();
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_functionmembervariable */
class FunctionMemberVariable {
/* class_functionmembervariable_onjoinchannelsuccess */
    final void Function(RtcConnection connection, int elapsed)?
        onJoinChannelSuccess;

/* api_functionmembervariable_memberfunction */
    Future<void> memberFunction();
}

/* class_functionmembervariable2 */
class FunctionMemberVariable2 {
/* class_functionmembervariable2_onjoinchannelsuccess */
    final void Function(RtcConnection connection, int elapsed)?
        onJoinChannelSuccess;

/* api_functionmembervariable2_memberfunction */
    Future<void> memberFunction();
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchClass(self):
        path = "match_cass.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
class ClassWithMixin
    with TheMixin
    implements TheInterface {

}

abstract class ClassWithExtendsAndImplements extends ParentClass
    implements TheInterface {

}

class ClassWithExtends extends ParentClass {

}

abstract class AbstractClass {

}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_classwithmixin */
class ClassWithMixin
    with TheMixin
    implements TheInterface {

}

/* class_classwithextendsandimplements */
abstract class ClassWithExtendsAndImplements extends ParentClass
    implements TheInterface {

}

/* class_classwithextends */
class ClassWithExtends extends ParentClass {

}

/* class_abstractclass */
abstract class AbstractClass {

}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchClassWithComment(self):
        path = "match_cass.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
/// Comment1
/// Comment2
class ClassWithMixin
    with TheMixin
    implements TheInterface {

}

/// Comment1
/// Comment2
abstract class ClassWithExtendsAndImplements extends ParentClass
    implements TheInterface {

}

/// Comment1
/// Comment2
class ClassWithExtends extends ParentClass {

}

/// Comment1
/// Comment2
abstract class AbstractClass {

}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_classwithmixin */
class ClassWithMixin
    with TheMixin
    implements TheInterface {

}

/* class_classwithextendsandimplements */
abstract class ClassWithExtendsAndImplements extends ParentClass
    implements TheInterface {

}

/* class_classwithextends */
class ClassWithExtends extends ParentClass {

}

/* class_abstractclass */
abstract class AbstractClass {

}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchClassWithAnnotations(self):
        path = "match_cass.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
@JsonSerializable(explicitToJson: true)
class AudioOptionsExternal {
  const AudioOptionsExternal(
      {this.enableAecExternalCustom,
      this.enableAgcExternalCustom,
      this.enableAnsExternalCustom,
      this.aecAggressivenessExternalCustom,
      this.enableAecExternalLoopback});

  @JsonKey(name: 'enable_aec_external_custom_')
  final bool? enableAecExternalCustom;

  @JsonKey(name: 'enable_agc_external_custom_')
  final bool? enableAgcExternalCustom;

  @JsonKey(name: 'enable_ans_external_custom_')
  final bool? enableAnsExternalCustom;

  @JsonKey(name: 'aec_aggressiveness_external_custom_')
  final NlpAggressiveness? aecAggressivenessExternalCustom;

  @JsonKey(name: 'enable_aec_external_loopback_')
  final bool? enableAecExternalLoopback;
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_audiooptionsexternal */
@JsonSerializable(explicitToJson: true)
class AudioOptionsExternal {
/* construct_audiooptionsexternal_audiooptionsexternal */
  const AudioOptionsExternal(
      {this.enableAecExternalCustom,
      this.enableAgcExternalCustom,
      this.enableAnsExternalCustom,
      this.aecAggressivenessExternalCustom,
      this.enableAecExternalLoopback});

/* class_audiooptionsexternal_enableaecexternalcustom */
  @JsonKey(name: 'enable_aec_external_custom_')
  final bool? enableAecExternalCustom;

/* class_audiooptionsexternal_enableagcexternalcustom */
  @JsonKey(name: 'enable_agc_external_custom_')
  final bool? enableAgcExternalCustom;

/* class_audiooptionsexternal_enableansexternalcustom */
  @JsonKey(name: 'enable_ans_external_custom_')
  final bool? enableAnsExternalCustom;

/* class_audiooptionsexternal_aecaggressivenessexternalcustom */
  @JsonKey(name: 'aec_aggressiveness_external_custom_')
  final NlpAggressiveness? aecAggressivenessExternalCustom;

/* class_audiooptionsexternal_enableaecexternalloopback */
  @JsonKey(name: 'enable_aec_external_loopback_')
  final bool? enableAecExternalLoopback;
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchClassMultiClasses(self):
        path = "match_cass.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
class AudioOptionsExternal {
  const AudioOptionsExternal(
      {this.enableAecExternalCustom,
      this.enableAgcExternalCustom,
      this.enableAnsExternalCustom,
      this.aecAggressivenessExternalCustom,
      this.enableAecExternalLoopback});

  final bool? enableAecExternalCustom;

  final bool? enableAgcExternalCustom;

  final bool? enableAnsExternalCustom;

  final NlpAggressiveness? aecAggressivenessExternalCustom;

  final bool? enableAecExternalLoopback;
}

class AudioOptionsExternal2 {
  const AudioOptionsExternal2(
      {this.enableAecExternalCustom,
      this.enableAgcExternalCustom,
      this.enableAnsExternalCustom,
      this.aecAggressivenessExternalCustom,
      this.enableAecExternalLoopback});

  final bool? enableAecExternalCustom;

  final bool? enableAgcExternalCustom;

  final bool? enableAnsExternalCustom;

  final NlpAggressiveness? aecAggressivenessExternalCustom;

  final bool? enableAecExternalLoopback;
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_audiooptionsexternal */
class AudioOptionsExternal {
/* construct_audiooptionsexternal_audiooptionsexternal */
  const AudioOptionsExternal(
      {this.enableAecExternalCustom,
      this.enableAgcExternalCustom,
      this.enableAnsExternalCustom,
      this.aecAggressivenessExternalCustom,
      this.enableAecExternalLoopback});

/* class_audiooptionsexternal_enableaecexternalcustom */
  final bool? enableAecExternalCustom;

/* class_audiooptionsexternal_enableagcexternalcustom */
  final bool? enableAgcExternalCustom;

/* class_audiooptionsexternal_enableansexternalcustom */
  final bool? enableAnsExternalCustom;

/* class_audiooptionsexternal_aecaggressivenessexternalcustom */
  final NlpAggressiveness? aecAggressivenessExternalCustom;

/* class_audiooptionsexternal_enableaecexternalloopback */
  final bool? enableAecExternalLoopback;
}

/* class_audiooptionsexternal2 */
class AudioOptionsExternal2 {
/* construct_audiooptionsexternal2_audiooptionsexternal2 */
  const AudioOptionsExternal2(
      {this.enableAecExternalCustom,
      this.enableAgcExternalCustom,
      this.enableAnsExternalCustom,
      this.aecAggressivenessExternalCustom,
      this.enableAecExternalLoopback});

/* class_audiooptionsexternal2_enableaecexternalcustom */
  final bool? enableAecExternalCustom;

/* class_audiooptionsexternal2_enableagcexternalcustom */
  final bool? enableAgcExternalCustom;

/* class_audiooptionsexternal2_enableansexternalcustom */
  final bool? enableAnsExternalCustom;

/* class_audiooptionsexternal2_aecaggressivenessexternalcustom */
  final NlpAggressiveness? aecAggressivenessExternalCustom;

/* class_audiooptionsexternal2_enableaecexternalloopback */
  final bool? enableAecExternalLoopback;
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchNonConstConstructor(self):
        path = "match_cass.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
class VideoViewController
    with VideoViewControllerBaseMixin
    implements VideoViewControllerBase {
  VideoViewController(
      {required this.rtcEngine,
      required this.canvas,
      this.useFlutterTexture = false,
      this.useAndroidSurfaceView = false})
      : connection = const RtcConnection();

  VideoViewController.remote(
      {required this.rtcEngine,
      required this.canvas,
      required this.connection,
      this.useFlutterTexture = false,
      this.useAndroidSurfaceView = false})
      : assert(connection.channelId != null);
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_videoviewcontroller */
class VideoViewController
    with VideoViewControllerBaseMixin
    implements VideoViewControllerBase {
/* construct_videoviewcontroller_videoviewcontroller */
  VideoViewController(
      {required this.rtcEngine,
      required this.canvas,
      this.useFlutterTexture = false,
      this.useAndroidSurfaceView = false})
      : connection = const RtcConnection();

/* construct_videoviewcontroller_remote */
  VideoViewController.remote(
      {required this.rtcEngine,
      required this.canvas,
      required this.connection,
      this.useFlutterTexture = false,
      this.useAndroidSurfaceView = false})
      : assert(connection.channelId != null);
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchEnum(self):
        path = "match_cass.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
@JsonEnum(alwaysCreate: true)
enum BackgroundSourceType {
  @JsonValue(1)
  backgroundColor,

  @JsonValue(2)
  backgroundImg,

  @JsonValue(3)
  backgroundBlur,
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* enum_backgroundsourcetype */
@JsonEnum(alwaysCreate: true)
enum BackgroundSourceType {
/* enum_backgroundsourcetype_backgroundcolor */
  @JsonValue(1)
  backgroundColor,

/* enum_backgroundsourcetype_backgroundimg */
  @JsonValue(2)
  backgroundImg,

/* enum_backgroundsourcetype_backgroundblur */
  @JsonValue(3)
  backgroundBlur,
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchTopLevelFunction(self):
        path = "match_cass.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
RtcEngine createAgoraRtcEngine() {
  return impl.RtcEngineImpl.create();
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* api_createagorartcengine */
RtcEngine createAgoraRtcEngine() {
  return impl.RtcEngineImpl.create();
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchTopLevelConstant(self):
        path = "match_cass.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
const String stringConst = "const string";

const stringConst2 = "const string";
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* constant_stringconst */
const String stringConst = "const string";

/* constant_stringconst2 */
const stringConst2 = "const string";
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchExtension(self):
        path = "match_cass.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
extension RtcEngineExt on RtcEngine {
  Future<String?> getAssetAbsolutePath(String assetPath) async {
    final impl = this as RtcEngineImpl;
    final p = await impl.engineMethodChannel
        .invokeMethod<String>('getAssetAbsolutePath', assetPath);
    return p;
  }
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/// @nodoc
extension RtcEngineExt on RtcEngine {
/* api_rtcengineext_getassetabsolutepath */
  Future<String?> getAssetAbsolutePath(String assetPath) async {
    final impl = this as RtcEngineImpl;
    final p = await impl.engineMethodChannel
        .invokeMethod<String>('getAssetAbsolutePath', assetPath);
    return p;
  }
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchConstructor(self):
        path = "match_cass.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
class Size {
  const Size({this.width, this.height});

  factory Size.fromJson(Map<String, dynamic> json) => _$SizeFromJson(json);
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_size */
class Size {
/* construct_size_size */
  const Size({this.width, this.height});

/// @nodoc
  factory Size.fromJson(Map<String, dynamic> json) => _$SizeFromJson(json);
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_tagOnAnnotation(self):
        path = "match_cass.dart"

        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
class Size {
  @override
  final VideoCanvas canvas;

  @protected
  void ss() {

  }
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_size */
class Size {
  @override
  final VideoCanvas canvas;

  @protected
  void ss() {

  }
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)


if __name__ == '__main__':
    unittest.main()
