import subprocess
from typing import Any

from iris_doc.post_phase import PostPhase


class PostPhaseTS(PostPhase):

    __executePath: str

    def __init__(self, executePath: str) -> None:
        self.__executePath = executePath

    def run(self) -> Any:
        p = subprocess.Popen(
            ["yarn", "run", "eslint", "--ext", ".js,.ts,.tsx", ".", "--fix"],
            cwd=self.__executePath)
        p.wait()
