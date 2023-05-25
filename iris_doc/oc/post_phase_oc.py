import os
from typing import Any, List
from typing import Any

from iris_doc.post_phase import PostPhase

class PostPhaseObjC(PostPhase):

    __executePath: str

    def __init__(self, executePath: str) -> None:
        self.__executePath = executePath

    def run(self) -> Any:
        print("Running Post Phase")
        export_file_dir = self.__executePath
        files: List[str] = []

        file_list = os.listdir(export_file_dir)
        for file in file_list:
            if file.endswith(".h"):
                files.append(os.path.join(export_file_dir, file))

        for file in files:
            os.system("clang-format -i " + file)
