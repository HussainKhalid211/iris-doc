import fs.memoryfs
import unittest
from iris_doc.api_tagger import ApiTagger, TagBuilder
from iris_doc.ts.api_tagger_ts import TSTagBuilder


class TestApiTaggerTS(unittest.TestCase):

    __fileSystem: fs.memoryfs.MemoryFS
    __apiTagger: ApiTagger

    @classmethod
    def setUpClass(self):
        self.__fileSystem = fs.memoryfs.MemoryFS()
        self.__apiTagger = ApiTagger(
            self.__fileSystem, TSTagBuilder())

    @classmethod
    def tearDownClass(self):
        self.__fileSystem.close()

    def test_matchMemberFunction(self):
        path = "member_function.ts"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
export abstract class IRtcEngine {
    abstract release(sync?: boolean): void;

    abstract setBeautyEffectOptions(
      enabled: boolean,
      options: BeautyOptions,
      type?: MediaSourceType
    ): number;

    onJoinChannelSuccess?(connection: RtcConnection, elapsed: number): void;
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_irtcengine */
export abstract class IRtcEngine {
/* api_irtcengine_release */
    abstract release(sync?: boolean): void;

/* api_irtcengine_setbeautyeffectoptions */
    abstract setBeautyEffectOptions(
      enabled: boolean,
      options: BeautyOptions,
      type?: MediaSourceType
    ): number;

/* api_irtcengine_onjoinchannelsuccess */
    onJoinChannelSuccess?(connection: RtcConnection, elapsed: number): void;
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchMemberFunctionWithBody(self):
        path = "member_function.ts"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
class MemberFunction {
  getMediaPlayerId(): number {
    const apiType = 'MediaPlayer_getMediaPlayerId';
    const jsonParams = {};
    const jsonResults = callIrisApi.call(this, apiType, jsonParams);
    return jsonResults.result;
  }

  play(): number {
    const apiType = 'MediaPlayer_play';
    const jsonParams = {};
    const jsonResults = callIrisApi.call(this, apiType, jsonParams);
    return jsonResults.result;
  }
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_memberfunction */
class MemberFunction {
/* api_memberfunction_getmediaplayerid */
  getMediaPlayerId(): number {
    const apiType = 'MediaPlayer_getMediaPlayerId';
    const jsonParams = {};
    const jsonResults = callIrisApi.call(this, apiType, jsonParams);
    return jsonResults.result;
  }

/* api_memberfunction_play */
  play(): number {
    const apiType = 'MediaPlayer_play';
    const jsonParams = {};
    const jsonResults = callIrisApi.call(this, apiType, jsonParams);
    return jsonResults.result;
  }
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchMemberVariablesAndMemberFunctions(self):
        path = "function_member_variables_and_member_functions.dart"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
class MemberVariableAndFunctions {
  stopMicrophoneRecording?: boolean;

  abstract release(sync?: boolean): void;
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_membervariableandfunctions */
class MemberVariableAndFunctions {
/* class_membervariableandfunctions_stopmicrophonerecording */
  stopMicrophoneRecording?: boolean;

/* api_membervariableandfunctions_release */
  abstract release(sync?: boolean): void;
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchClass(self):
        path = "match_cass.ts"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
export class IMediaPlayerImpl implements IMediaPlayer {

}

export class IRtcEngineExImpl extends IRtcEngineImpl implements IRtcEngineEx {

}

export abstract class AbstractClass {

}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_imediaplayerimpl */
export class IMediaPlayerImpl implements IMediaPlayer {

}

/* class_irtcengineeximpl */
export class IRtcEngineExImpl extends IRtcEngineImpl implements IRtcEngineEx {

}

/* class_abstractclass */
export abstract class AbstractClass {

}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchClassWithComment(self):
        path = "match_cass.ts"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
/*
 * Comment1
 */
export class IMediaPlayerImpl implements IMediaPlayer {

}

/*
 * Comment1
 */
export class IRtcEngineExImpl extends IRtcEngineImpl implements IRtcEngineEx {

}

/*
 * Comment1
 */
export abstract class AbstractClass {

}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_imediaplayerimpl */
export class IMediaPlayerImpl implements IMediaPlayer {

}

/* class_irtcengineeximpl */
export class IRtcEngineExImpl extends IRtcEngineImpl implements IRtcEngineEx {

}

/* class_abstractclass */
export abstract class AbstractClass {

}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchClassMultiClasses(self):
        path = "match_cass.ts"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
export class LiveStreamAdvancedFeature {
  featureName?: string;

  opened?: boolean;
}

export class livestreamadvancedfeature2 {
  featureName?: string;

  opened?: boolean;
}

export class livestreamadvancedfeature3 {
  featureName?: string;
  opened?: boolean;
  opened2?: boolean;
  opened3?: boolean;
  opened4?: boolean;
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* class_livestreamadvancedfeature */
export class LiveStreamAdvancedFeature {
/* class_livestreamadvancedfeature_featurename */
  featureName?: string;

/* class_livestreamadvancedfeature_opened */
  opened?: boolean;
}

/* class_livestreamadvancedfeature2 */
export class livestreamadvancedfeature2 {
/* class_livestreamadvancedfeature2_featurename */
  featureName?: string;

/* class_livestreamadvancedfeature2_opened */
  opened?: boolean;
}

/* class_livestreamadvancedfeature3 */
export class livestreamadvancedfeature3 {
/* class_livestreamadvancedfeature3_featurename */
  featureName?: string;
/* class_livestreamadvancedfeature3_opened */
  opened?: boolean;
/* class_livestreamadvancedfeature3_opened2 */
  opened2?: boolean;
/* class_livestreamadvancedfeature3_opened3 */
  opened3?: boolean;
/* class_livestreamadvancedfeature3_opened4 */
  opened4?: boolean;
}
        """
        processedContent = self.__fileSystem.readtext(path)
        print(f'result\n{processedContent}')
        self.assertEqual(processedContent, expectedContent)

    def test_matchEnum(self):
        path = "match_cass.ts"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
export enum AudioRecordingQualityType {
  AudioRecordingQualityLow = 0,

  AudioRecordingQualityMedium = 1,

  AudioRecordingQualityHigh = 2,
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* enum_audiorecordingqualitytype */
export enum AudioRecordingQualityType {
/* enum_audiorecordingqualitytype_audiorecordingqualitylow */
  AudioRecordingQualityLow = 0,

/* enum_audiorecordingqualitytype_audiorecordingqualitymedium */
  AudioRecordingQualityMedium = 1,

/* enum_audiorecordingqualitytype_audiorecordingqualityhigh */
  AudioRecordingQualityHigh = 2,
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchTopLevelFunction(self):
        path = "match_cass.dart"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
function greeter(fn: (a: string) => void) {
  fn("Hello, World");
}
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* api_greeter */
function greeter(fn: (a: string) => void) {
  fn("Hello, World");
}
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)

    def test_matchTopLevelConstant(self):
        path = "match_cass.dart"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
const AgoraRtcSurfaceView = requireNativeComponent<{ callApi: object }>(
  'AgoraRtcSurfaceView'
);
        """)
        file.flush()
        file.close()
        self.__apiTagger.process(path)

        expectedContent = """
/* constant_agorartcsurfaceview */
const AgoraRtcSurfaceView = requireNativeComponent<{ callApi: object }>(
  'AgoraRtcSurfaceView'
);
        """
        processedContent = self.__fileSystem.readtext(path)
        self.assertEqual(processedContent, expectedContent)


if __name__ == '__main__':
    unittest.main()
