import fs.memoryfs
import unittest

from iris_doc.language_specification import LanguageSpecificationModule, LanguageSpecificationConfig


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
        "id": "callback_onfirstremotevideoframe",
        "name": "onFirstRemoteVideoFrame",
        "description": "Occurs when the renderer receives the first frame of the remote video.",
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
        # module.setLanguageSpecificationConfig(languageSpecificationConfig)
        module.read_template_file(path)
        module.deserialize()

        commentSources = module.getAllCommentSources()

        self.assertEqual(len(commentSources.keys()), 2)
        self.assertIn(
            "class_rtcengineeventhandler_onfirstremotevideoframe", commentSources.keys())
        self.assertIn("class_rtcengineeventhandler", commentSources.keys())


if __name__ == '__main__':
    unittest.main()
