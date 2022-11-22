import os
import subprocess
from typing import Any, List

from iris_doc.post_phase import PostPhase

class PostPhaseCSharp(PostPhase):

    __executePath: str

    def __init__(self, executePath: str) -> None:
        self.__executePath = executePath

    def run(self) -> Any:
        export_file_dir = os.path.join(self.__executePath, "Rtc")
        files: List[str] = []

        file_list = os.listdir(export_file_dir)
        for file in file_list:
            if file.endswith(".cs"):
                files.append(os.path.join(export_file_dir, file))

        type_dir = os.path.join(export_file_dir, "Types")
        file_list = os.listdir(type_dir)
        for file in file_list:
            if file.endswith(".cs"):
                files.append(os.path.join(type_dir, file))

        files.append(os.path.join(export_file_dir, "VideoRender/VideoSurface.cs"))
        files.append(os.path.join(export_file_dir, "VideoRender/VideoSurfaceYUV.cs"))

        for file in files:
            os.system("clang-format -i " + file)

