import unittest

import fs.memoryfs

from iris_doc.dart.api_tagger_dart import DartTagBuilder
from iris_doc.iris_doc_cli import _processExportFile
from iris_doc.language_specification import LanguageSpecificationConfig
from iris_doc.post_phase import DefaultPostPhase
from iris_doc.test.fake_export_file_parser import FakeExportFileParser


class TestIrisDocCliDart(unittest.TestCase):
    __fileSystem: fs.memoryfs.MemoryFS

    @classmethod
    def setUp(cls):
        cls.__fileSystem = fs.memoryfs.MemoryFS()

    @classmethod
    def tearDown(cls):
        cls.__fileSystem.close()

    def test_tag2doc_member_function(self):
        config_file_path = "fmt_dart.yaml"
        self.__fileSystem.create(config_file_path, wipe=True)
        config_file = self.__fileSystem.open(config_file_path, mode="w")
        config_file.write("""
comment1: ""
comment2: "///"
comment3: ""
summary1: ""
summary2: ""
tag1: "**"
tag2: "**"
param1: "* ["
param2: "] "
param3: ""
link1: "["
link2: "]"
ignore: "@nodoc"
return1: Returns
return2: ""
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
                "name": "RtcEngine",
                "description": "The basic interface of the Agora SDK that implements the core functions of real-time communication.",
                "parameters": [],
                "returns": "",
                "is_hide": false
            },
            {
                "id": "api_irtcengine_enabledualstreammode2",
                "name": "enableDualStreamMode [2/3]",
                "description": "Enables or disables dual-stream mode.",
                "parameters": [
                    {
                        "sourceType": "The capture type of the custom video source. See VideoSourceType ."
                    },
                    {
                        "enabled": "Whether to enable dual-stream mode:true: Enable dual-stream mode.false: Disable dual-stream mode."
                    }
                ],
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
                "returns": "",
                "is_hide": false
            },
            {
                "id": "api_irtcengine_stoprhythmplayer",
                "name": "stopRhythmPlayer",
                "description": "Disables the virtual metronome.",
                "parameters": [],
                "returns": "",
                "is_hide": false
            },
           {
                "id": "api_irtcengine_setsubscribeaudioallowlist",
                "name": "setSubscribeAudioAllowlist",
                "description": "Sets the allowlist of subscriptions for audio streams.",
                "parameters": [
                    {
                        "uidList": "The user ID list of users that you want to subscribe to."
                    },
                    {
                        "uidNumber": "The number of users in the user ID list."
                    }
                ],
                "returns": "",
                "is_hide": false
            }
        ]
                """)
        json_file.flush()
        json_file.close()

        dart_file_path = "member_function.dart"

        self.__fileSystem.create(dart_file_path, wipe=True)
        file = self.__fileSystem.open(dart_file_path, mode="w")
        file.write("""
class RtcEngine {
  Future<void> stopRhythmPlayer();

  Future<void> enableDualStreamMode(
      {required bool enabled, SimulcastStreamConfig? streamConfig});

  Future<void> setSubscribeAudioAllowlist(
      {required List<int> uidList, required int uidNumber});
}
        """)
        file.flush()
        file.close()

        fakeExportFileParser = FakeExportFileParser([dart_file_path])

        languageSpecificationConfig: LanguageSpecificationConfig = LanguageSpecificationConfig(
            isCallback2class=True,
            isCallback2api=False,
            idPatternV2=True)

        _processExportFile(languageSpecificationConfig=languageSpecificationConfig,
                           configPath=config_file_path,
                           tagBuilder=DartTagBuilder(),
                           exportFileParser=fakeExportFileParser,
                           postPhase=DefaultPostPhase(),
                           exportFilePath="",
                           templateFilePathList=[json_file_path],
                           fileSystem=self.__fileSystem,
                           isForceMarkNoDoc=False
                           )

        result = self.__fileSystem.readtext(dart_file_path)

        expected_content = """
/// The basic interface of the Agora SDK that implements the core functions of real-time communication.
class RtcEngine {
/// Disables the virtual metronome.
  Future<void> stopRhythmPlayer();

/// Enables or disables the dual-stream mode on the sender and sets the low-quality video stream.
///
/// * [enabled] Whether to enable dual-stream mode:true: Enable dual-stream mode.false: (Default) Disable dual-stream mode.
/// * [streamConfig] The configuration of the low-quality video stream. See SimulcastStreamConfig .
  Future<void> enableDualStreamMode(
      {required bool enabled, SimulcastStreamConfig? streamConfig});

/// Sets the allowlist of subscriptions for audio streams.
///
/// * [uidList] The user ID list of users that you want to subscribe to.
/// * [uidNumber] The number of users in the user ID list.
  Future<void> setSubscribeAudioAllowlist(
      {required List<int> uidList, required int uidNumber});
}
        """
        self.assertEqual(result, expected_content)

    def test_tag2doc_member_function_parameters_random_order(self):
        config_file_path = "fmt_dart.yaml"
        self.__fileSystem.create(config_file_path, wipe=True)
        config_file = self.__fileSystem.open(config_file_path, mode="w")
        config_file.write("""
comment1: ""
comment2: "///"
comment3: ""
summary1: ""
summary2: ""
tag1: "**"
tag2: "**"
param1: "* ["
param2: "] "
param3: ""
link1: "["
link2: "]"
ignore: "@nodoc"
return1: Returns
return2: ""
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
                "name": "RtcEngine",
                "description": "The basic interface of the Agora SDK that implements the core functions of real-time communication.",
                "parameters": [],
                "returns": "",
                "is_hide": false
            },
            {
                "id": "api_irtcengine_enabledualstreammode2",
                "name": "enableDualStreamMode [2/3]",
                "description": "Enables or disables dual-stream mode.",
                "parameters": [
                    {
                        "sourceType": "The capture type of the custom video source. See VideoSourceType ."
                    },
                    {
                        "enabled": "Whether to enable dual-stream mode:true: Enable dual-stream mode.false: Disable dual-stream mode."
                    }
                ],
                "returns": "",
                "is_hide": false
            },
            {
                "id": "api_irtcengine_enabledualstreammode3",
                "name": "enableDualStreamMode",
                "description": "Enables or disables the dual-stream mode on the sender and sets the low-quality video stream.",
                "parameters": [
                    {
                        "streamConfig": "The configuration of the low-quality video stream. See SimulcastStreamConfig ."
                    },
                    {
                        "enabled": "Whether to enable dual-stream mode:true: Enable dual-stream mode.false: (Default) Disable dual-stream mode."
                    }
                ],
                "returns": "",
                "is_hide": false
            }
        ]
                """)
        json_file.flush()
        json_file.close()

        dart_file_path = "member_function.dart"

        self.__fileSystem.create(dart_file_path, wipe=True)
        file = self.__fileSystem.open(dart_file_path, mode="w")
        file.write("""
class RtcEngine {
  Future<void> enableDualStreamMode(
      {required bool enabled, SimulcastStreamConfig? streamConfig});
}
        """)
        file.flush()
        file.close()

        fakeExportFileParser = FakeExportFileParser([dart_file_path])

        languageSpecificationConfig: LanguageSpecificationConfig = LanguageSpecificationConfig(
            isCallback2class=True,
            isCallback2api=False,
            idPatternV2=True)

        _processExportFile(languageSpecificationConfig=languageSpecificationConfig,
                           configPath=config_file_path,
                           tagBuilder=DartTagBuilder(),
                           exportFileParser=fakeExportFileParser,
                           postPhase=DefaultPostPhase(),
                           exportFilePath="",
                           templateFilePathList=[json_file_path],
                           fileSystem=self.__fileSystem,
                           isForceMarkNoDoc=False
                           )

        result = self.__fileSystem.readtext(dart_file_path)

        expected_content = """
/// The basic interface of the Agora SDK that implements the core functions of real-time communication.
class RtcEngine {
/// Enables or disables the dual-stream mode on the sender and sets the low-quality video stream.
///
/// * [enabled] Whether to enable dual-stream mode:true: Enable dual-stream mode.false: (Default) Disable dual-stream mode.
/// * [streamConfig] The configuration of the low-quality video stream. See SimulcastStreamConfig .
  Future<void> enableDualStreamMode(
      {required bool enabled, SimulcastStreamConfig? streamConfig});
}
        """
        self.assertEqual(result, expected_content)

    def test_tag2doc_function_as_member_variables(self):
        config_file_path = "fmt_dart.yaml"
        self.__fileSystem.create(config_file_path, wipe=True)
        config_file = self.__fileSystem.open(config_file_path, mode="w")
        config_file.write("""
comment1: ""
comment2: "///"
comment3: ""
summary1: ""
summary2: ""
tag1: "**"
tag2: "**"
param1: "* ["
param2: "] "
param3: ""
link1: "["
link2: "]"
ignore: "@nodoc"
return1: Returns
return2: ""
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
                "name": "RtcEngineEventHandler",
                "description": "RtcEngineEventHandlerThe SDK uses the interface to send event notifications to your app.",
                "parameters": [],
                "returns": "",
                "is_hide": false
            },
            {
                "id": "callback_irtcengineeventhandler_onnetworktypechanged",
                "name": "onNetworkTypeChanged",
                "description": "Occurs when the local network type changes.",
                "parameters": [
                    {
                        "connection": "The connection information. See RtcConnection ."
                    },
                    {
                        "type": "The type of the local network connection. See NetworkType ."
                    }
                ],
                "returns": "",
                "is_hide": false
            }
        ]
                """)
        json_file.flush()
        json_file.close()

        dart_file_path = "member_function.dart"

        self.__fileSystem.create(dart_file_path, wipe=True)
        file = self.__fileSystem.open(dart_file_path, mode="w")
        file.write("""
class RtcEngineEventHandler {
  final void Function(RtcConnection connection, NetworkType type)?
      onNetworkTypeChanged;
}
        """)
        file.flush()
        file.close()

        fakeExportFileParser = FakeExportFileParser([dart_file_path])

        languageSpecificationConfig: LanguageSpecificationConfig = LanguageSpecificationConfig(
            isCallback2class=True,
            isCallback2api=False,
            idPatternV2=True)

        _processExportFile(languageSpecificationConfig=languageSpecificationConfig,
                           configPath=config_file_path,
                           tagBuilder=DartTagBuilder(),
                           exportFileParser=fakeExportFileParser,
                           postPhase=DefaultPostPhase(),
                           exportFilePath="",
                           templateFilePathList=[json_file_path],
                           fileSystem=self.__fileSystem,
                           isForceMarkNoDoc=False
                           )

        result = self.__fileSystem.readtext(dart_file_path)

        expected_content = """
/// RtcEngineEventHandlerThe SDK uses the interface to send event notifications to your app.
class RtcEngineEventHandler {
/// Occurs when the local network type changes.
///
/// * [connection] The connection information. See RtcConnection .
/// * [type] The type of the local network connection. See NetworkType .
  final void Function(RtcConnection connection, NetworkType type)?
      onNetworkTypeChanged;
}
        """
        self.assertEqual(result, expected_content)


if __name__ == '__main__':
    unittest.main()
