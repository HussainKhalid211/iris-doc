import subprocess
from typing import Any

from iris_doc.post_phase import PostPhase


class PostPhaseTS(PostPhase):

    __executePath: str

    def __init__(self, executePath: str) -> None:
        self.__executePath = executePath

    def run(self) -> Any:
        p = subprocess.Popen(
            ["yarn", "install", "--frozen-lockfile"],
            cwd=self.__executePath)
        p.wait()
        p = subprocess.Popen(
            ["yarn", "patch-package"],
            cwd=self.__executePath)
        p.wait()
        p = subprocess.Popen(
            ["yarn", "eslint", "--ext", ".js,.ts,.tsx", ".", "--fix"],
            cwd=self.__executePath)
        p.wait()
