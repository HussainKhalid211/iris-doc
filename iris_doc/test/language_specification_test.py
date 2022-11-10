import fs.memoryfs
import unittest

from iris_doc.language_specification import CommentSource, LanguageSpecificationModule, LanguageSpecificationConfig


class TestLanguageSpecificationModule(unittest.TestCase):

    __fileSystem: fs.memoryfs.MemoryFS

    @classmethod
    def setUpClass(self):
        self.__fileSystem = fs.memoryfs.MemoryFS()

    @classmethod
    def tearDownClass(self):
        self.__fileSystem.close()

    def testMatchTagPatternV2(self):
        path = "template.json"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
[
    {
        "id": "class_irtcengineeventhandler",
        "name": "RtcEngineEventHandler",
        "description": "The SDK uses the RtcEngineEventHandler interface",
        "parameters": [],
        "returns": "",
        "is_hide": false
    },
    {
        "id": "callback_irtcengineeventhandler_onfirstremotevideoframe",
        "name": "onFirstRemoteVideoFrame",
        "description": "Occurs when the renderer receives the first frame of the remote video.",
        "parameters": [
        ],
        "returns": "",
        "is_hide": false
    },
    {
        "id": "class_rtcengineconfig_ng",
        "name": "RtcEngineContext",
        "description": "Definition of RtcEngineContext.",
        "parameters": [
        ],
        "returns": "",
        "is_hide": false
    }
]
        """)
        file.flush()
        file.close()

        languageSpecificationConfig: LanguageSpecificationConfig = LanguageSpecificationConfig(
            isCallback2class=True,
            isCallback2api=False,
            idPatternV2=True)

        module = LanguageSpecificationModule(
            self.__fileSystem, languageSpecificationConfig)
        module.addTemplateFilePath(path)
        module.deserialize()

        commentSources = module.getAllCommentSources()

        self.assertEqual(len(commentSources.keys()), 3)
        self.assertIn(
            "class_rtcengineeventhandler_onfirstremotevideoframe", commentSources.keys())
        self.assertIn("class_rtcengineeventhandler", commentSources.keys())
        self.assertIn("class_rtcenginecontext", commentSources.keys())

    def testMultipleTemplateFile(self):
        path = "template.json"
        self.__fileSystem.create(path, wipe=True)
        file = self.__fileSystem.open(path, mode="w")
        file.write("""
[
    {
        "id": "class_irtcengineeventhandler",
        "name": "RtcEngineEventHandler",
        "description": "The SDK uses the RtcEngineEventHandler interface",
        "parameters": [],
        "returns": "",
        "is_hide": false
    },
    {
        "id": "callback_irtcengineeventhandler_onfirstremotevideoframe",
        "name": "onFirstRemoteVideoFrame",
        "description": "Occurs when the renderer receives the first frame of the remote video.",
        "parameters": [
        ],
        "returns": "",
        "is_hide": false
    },
    {
        "id": "class_rtcengineconfig_ng",
        "name": "RtcEngineContext",
        "description": "Definition of RtcEngineContext.",
        "parameters": [
        ],
        "returns": "",
        "is_hide": false
    }
]
        """)
        file.flush()
        file.close()

        path2 = "template.json"
        self.__fileSystem.create(path2, wipe=True)
        file2 = self.__fileSystem.open(path2, mode="w")
        file2.write("""
[
    {
        "id": "class_irtcengineeventhandler",
        "name": "RtcEngineEventHandler",
        "description": "The RtcEngineEventHandler interface",
        "parameters": [],
        "returns": "",
        "is_hide": false
    },
    {
        "id": "callback_irtcengineeventhandler_onfirstremotevideoframe",
        "name": "onFirstRemoteVideoFrame",
        "description": "Occurs when the renderer receives the first frame of the remote video.",
        "parameters": [
        ],
        "returns": "",
        "is_hide": false
    },
    {
        "id": "class_rtmconfig",
        "name": "RtmConfig",
        "description": "Definition of RtmConfig.",
        "parameters": [
        ],
        "returns": "",
        "is_hide": false
    }
]
        """)
        file2.flush()
        file2.close()

        languageSpecificationConfig: LanguageSpecificationConfig = LanguageSpecificationConfig(
            isCallback2class=True,
            isCallback2api=False,
            idPatternV2=True)

        module = LanguageSpecificationModule(
            self.__fileSystem, languageSpecificationConfig)
        module.addTemplateFilePath(path)
        module.addTemplateFilePath(path2)
        module.deserialize()

        commentSources = module.getAllCommentSources()

        self.assertEqual(len(commentSources.keys()), 4)
        self.assertIn(
            "class_rtcengineeventhandler_onfirstremotevideoframe", commentSources.keys())
        self.assertIn("class_rtcengineeventhandler", commentSources.keys())

        comment: CommentSource = commentSources['class_rtcengineeventhandler']
        self.assertEqual(comment.description, 'The SDK uses the RtcEngineEventHandler interface')

        self.assertIn("class_rtcenginecontext", commentSources.keys())
        self.assertIn("class_rtmconfig", commentSources.keys())


if __name__ == '__main__':
    unittest.main()
