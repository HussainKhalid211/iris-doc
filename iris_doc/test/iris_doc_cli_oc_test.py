import unittest

import fs.memoryfs

from iris_doc.iris_doc_cli import _processExportFile
from iris_doc.language_specification import LanguageSpecificationConfig
from iris_doc.post_phase import DefaultPostPhase
from iris_doc.test.fake_export_file_parser import FakeExportFileParser
from iris_doc.oc.api_tagger_oc import ObjCTagBuilder


class TestIrisDocCliObjC(unittest.TestCase):
    __fileSystem: fs.memoryfs.MemoryFS

    @classmethod
    def setUp(cls):
        cls.__fileSystem = fs.memoryfs.MemoryFS()

    @classmethod
    def tearDown(cls):
        cls.__fileSystem.close()

    def test_tag2doc_member_function(self):
        config_file_path = "fmt_oc.yaml"
        self.__fileSystem.create(config_file_path, wipe=True)
        config_file = self.__fileSystem.open(config_file_path, mode="w")
        config_file.write("""
comment1: ""
comment2: "///"
comment3: ""
summary1: ""
summary2: ""
tag1: "> "
tag2: ""
param1: "- Parameter "
param2: ": "
param3: ""
link1: "``"
link2: "``"
ignore: "@ignore"
return1: ""
return2: "- Returns: "
return3: ""
""")

        config_file.flush()
        config_file.close()

        json_file_path = "testMultipleTemplateFile1.json"
        self.__fileSystem.create(json_file_path, wipe=True)
        json_file = self.__fileSystem.open(json_file_path, mode="w")
        json_file.write("""
        [
            {
                "id": "class_irtcengine",
                "name": "AgoraRtcEngineKit",
                "description": "The basic interface of the Agora SDK that implements the core functions of real-time communication.",
                "parameters": [],
                "returns": "",
                "is_hide": false
            },
            {
                "id": "api_irtcengine_enabledualstreammode3",
                "name": "enableDualStreamMode",
                "description": "Enables or disables the dual-stream mode on the sender and sets the low-quality video stream.",
                "parameters": [
                    {
                        "enabled": "Whether to enable dual-stream mode:true: Enable dual-stream mode.false: (Default) Disable dual-stream mode."
                    },
                    {
                        "streamConfig": "The configuration of the low-quality video stream. See SimulcastStreamConfig ."
                    }
                ],
                "returns": "An integer",
                "is_hide": false
            }
        ]
                """)
        json_file.flush()
        json_file.close()

        oc_file_path = "member_function.h"

        self.__fileSystem.create(oc_file_path, wipe=True)
        file = self.__fileSystem.open(oc_file_path, mode="w")
        file.write("""
@interface AgoraRtcEngineKit
- (int)enableDualStreamMode:(BOOL)enabled
    streamConfig:(AgoraSimulcastStreamConfig* _Nonnull)streamConfig NS_SWIFT_NAME(enableDualStreamMode(_:streamConfig:));
@end
        """)
        file.flush()
        file.close()

        fakeExportFileParser = FakeExportFileParser([oc_file_path])

        languageSpecificationConfig: LanguageSpecificationConfig = LanguageSpecificationConfig(
            isCallback2class=False,
            isCallback2api=True,
            idPatternV2=True)

        _processExportFile(languageSpecificationConfig=languageSpecificationConfig,
                           configPath=config_file_path,
                           tagBuilder=ObjCTagBuilder(),
                           exportFileParser=fakeExportFileParser,
                           postPhase=DefaultPostPhase(),
                           exportFilePath="",
                           templateFilePathList=[json_file_path],
                           fileSystem=self.__fileSystem,
                           isForceMarkNoDoc=False
                           )

        result = self.__fileSystem.readtext(oc_file_path)

        expected_content = """
/// The basic interface of the Agora SDK that implements the core functions of real-time communication.
@interface AgoraRtcEngineKit
/// Enables or disables the dual-stream mode on the sender and sets the low-quality video stream.
///
/// - Parameter enabled: Whether to enable dual-stream mode:true: Enable dual-stream mode.false: (Default) Disable dual-stream mode.
/// - Parameter streamConfig: The configuration of the low-quality video stream. See SimulcastStreamConfig .
///
/// - Returns: An integer
- (int)enableDualStreamMode:(BOOL)enabled
    streamConfig:(AgoraSimulcastStreamConfig* _Nonnull)streamConfig NS_SWIFT_NAME(enableDualStreamMode(_:streamConfig:));
@end
        """
        self.assertEqual(result, expected_content)

    def test_tag2doc_delegate(self):
        config_file_path = "fmt_oc.yaml"
        self.__fileSystem.create(config_file_path, wipe=True)
        config_file = self.__fileSystem.open(config_file_path, mode="w")
        config_file.write("""
comment1: ""
comment2: "///"
comment3: ""
summary1: ""
summary2: ""
tag1: "> "
tag2: ""
param1: "- Parameter "
param2: ": "
param3: ""
link1: "``"
link2: "``"
ignore: "@ignore"
return1: ""
return2: "- Returns: "
return3: ""
""")

        config_file.flush()
        config_file.close()

        json_file_path = "testMultipleTemplateFile1.json"
        self.__fileSystem.create(json_file_path, wipe=True)
        json_file = self.__fileSystem.open(json_file_path, mode="w")
        json_file.write("""
        [
            {
                "id": "class_irtcengineeventhandler",
                "name": "AgoraRtcEngineDelegate",
                "description": "The SDK uses the interface to send event notifications to your app. Your app can get those notifications through methods that inherit this interface.",
                "parameters": [],
                "returns": "",
                "is_hide": false
            }, {
                "id": "callback_irtcengineeventhandler_onrhythmplayerstatechanged",
                "name": "didRhythmPlayerStateChanged",
                "description": "Occurs when the state of virtual metronome changes. When the state of the virtual metronome changes, the SDK triggers this callback to report the current state of the virtual metronome. This callback indicates the state of the local audio stream and enables you to troubleshoot issues when audio exceptions occur.",
                "parameters": [
                    { "state": "For the current virtual metronome status, see AgoraRhythmPlayerState ." },
                    { "errorCode": "For the error codes and error messages related to virtual metronome errors, see AgoraRhythmPlayerError ." }
                ],
                "returns": "",
                "is_hide": false
            },
            {
                "id": "callback_irtcengineeventhandler_onfirstremotevideoframe",
                "name": "firstRemoteVideoFrameOfUid",
                "description": "Occurs when the renderer receives the first frame of the remote video.",
                "parameters": [ { "engine": "AgoraRtcEngineKit object." }, { "uid": "The ID of the remote user sending the video stream." }, { "size": "The video dimension." }, { "elapsed": "The time elapsed (ms) from the local user calling joinChannelByToken [2/4] until the SDK triggers this callback." } ], "returns": "", "is_hide": false
            }
        ]
                """)
        json_file.flush()
        json_file.close()

        oc_file_path = "delegate_function.h"

        self.__fileSystem.create(oc_file_path, wipe=True)
        file = self.__fileSystem.open(oc_file_path, mode="w")
        file.write("""
@protocol AgoraRtcEngineDelegate <NSObject>
@optional

- (void)rtcEngine:(AgoraRtcEngineKit *_Nonnull)engine
    didRhythmPlayerStateChanged:(AgoraRhythmPlayerState)state
                      errorCode:(AgoraRhythmPlayerError)errorCode
    NS_SWIFT_NAME(rtcEngine(_:didRhythmPlayerStateChanged:errorCode:));

- (void)rtcEngine:(AgoraRtcEngineKit * _Nonnull)engine firstRemoteVideoFrameOfUid:(NSUInteger)uid size:(CGSize)size elapsed:(NSInteger)elapsed NS_SWIFT_NAME(rtcEngine(_:firstRemoteVideoFrameOfUid:size:elapsed:));
@end
        """)
        file.flush()
        file.close()

        fakeExportFileParser = FakeExportFileParser([oc_file_path])

        languageSpecificationConfig: LanguageSpecificationConfig = LanguageSpecificationConfig(
            isCallback2class=False,
            isCallback2api=True,
            idPatternV2=True)

        _processExportFile(languageSpecificationConfig=languageSpecificationConfig,
                           configPath=config_file_path,
                           tagBuilder=ObjCTagBuilder(),
                           exportFileParser=fakeExportFileParser,
                           postPhase=DefaultPostPhase(),
                           exportFilePath="",
                           templateFilePathList=[json_file_path],
                           fileSystem=self.__fileSystem,
                           isForceMarkNoDoc=False
                           )

        result = self.__fileSystem.readtext(oc_file_path)

        expected_content = """
/// The SDK uses the interface to send event notifications to your app. Your app can get those notifications through methods that inherit this interface.
@protocol AgoraRtcEngineDelegate <NSObject>
@optional

/// Occurs when the state of virtual metronome changes. When the state of the virtual metronome changes, the SDK triggers this callback to report the current state of the virtual metronome. This callback indicates the state of the local audio stream and enables you to troubleshoot issues when audio exceptions occur.
///
/// - Parameter state: For the current virtual metronome status, see AgoraRhythmPlayerState .
/// - Parameter errorCode: For the error codes and error messages related to virtual metronome errors, see AgoraRhythmPlayerError .
- (void)rtcEngine:(AgoraRtcEngineKit *_Nonnull)engine
    didRhythmPlayerStateChanged:(AgoraRhythmPlayerState)state
                      errorCode:(AgoraRhythmPlayerError)errorCode
    NS_SWIFT_NAME(rtcEngine(_:didRhythmPlayerStateChanged:errorCode:));

/// Occurs when the renderer receives the first frame of the remote video.
///
/// - Parameter engine: AgoraRtcEngineKit object.
/// - Parameter uid: The ID of the remote user sending the video stream.
/// - Parameter size: The video dimension.
/// - Parameter elapsed: The time elapsed (ms) from the local user calling joinChannelByToken [2/4] until the SDK triggers this callback.
- (void)rtcEngine:(AgoraRtcEngineKit * _Nonnull)engine firstRemoteVideoFrameOfUid:(NSUInteger)uid size:(CGSize)size elapsed:(NSInteger)elapsed NS_SWIFT_NAME(rtcEngine(_:firstRemoteVideoFrameOfUid:size:elapsed:));
@end
        """
        self.assertEqual(result, expected_content)

if __name__ == '__main__':
    unittest.main()
