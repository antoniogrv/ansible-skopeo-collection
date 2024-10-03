"""
Execute a Skopeo command in an safe and orderded fashion.
"""

import subprocess


class SkopeoCommand:
    """
    SkopeoCommand represents a command executing using the Skopeo toolkit.
    """

    DEFAULT_SKOPEO_EXECUTABLE: str = "skopeo"

    def __init__(
        self,
        executable: str = DEFAULT_SKOPEO_EXECUTABLE,
        command: list[str] = None,
        timeout: int = 60,
    ) -> None:
        """Initializes a SkopeoCommand instance."""

        self.skopeo_executable: str = executable
        self.skopeo_command: list[str] = command

        self.timeout = timeout

        self.skopeo_execution: subprocess.CompletedProcess[bytes] = self.execute()

    def execute(self) -> subprocess.CompletedProcess[bytes]:
        """Executes a Skopeo command.

        Returns:
            subprocess.CompletedProcess[bytes]: Contains information about the execution.
        """
        return subprocess.run(
            [self.get_executable(), *self.get_command()],
            capture_output=True,
            timeout=self.timeout,
            check=False,
        )

    def get_executable(self) -> str:
        """Fetches the Skopeo CLI, as long as it is in the PATH.

        Returns:
            str: Returns the Skopeo CLI binary, e.g. "skopeo"
        """
        return self.skopeo_executable

    def get_command(self) -> list[str]:
        """Fetches the Skopeo command that the client wants to execute.

        Returns:
            list[str]: Returns the subcommand as the first item of the list,
                       then the arguments of the subcommand as subsequent list entries.
        """
        return self.skopeo_command

    def get_execution(self) -> subprocess.CompletedProcess[bytes]:
        """Grabs the Skopeo execution process in order to obtain additional information.

        Returns:
            subprocess.CompletedProcess[bytes]: Contains information about the execution.
        """
        return self.skopeo_execution

    def get_return_code(self) -> int:
        """Fetches the process return code.

        Returns:
            int: Returns the return code, e.g. 0 in case of success.
        """
        return self.get_execution().returncode

    def get_stdout(self) -> str:
        """Grabs the STDOUT process lines.

        Returns:
            str: STDOUT of the process.
        """
        return self.get_execution().stdout

    def get_stderr(self) -> str:
        """Grabs the STDERR process lines.

        Returns:
            str: STDERR of the process.
        """
        return self.get_execution().stderr

    def failed(self) -> bool:
        """Returns `False` if the command failed, `True` otherwise.

        Returns:
            bool: Either `True` or `False`.
        """
        return self.get_return_code() != 0

    def success(self) -> bool:
        """Returns `True` if the command succedeed, `False` otherwise.

        Returns:
            bool: Either `True` or `False`.
        """
        return self.get_return_code() == 0

    def __str__(self) -> str:
        """Prints the SkopeoCommand object.

        Returns:
            str: Displays information about the process execution.
        """
        return str(
            {
                "return_code": self.get_return_code(),
                "stdout": self.get_stdout(),
                "stderr": self.get_stderr(),
            }
        )
