import subprocess

class SkopeoCommand():
    DEFAULT_SKOPEO_EXECUTABLE: str = "skopeo"

    def __init__(
            self, 
            executable: str = DEFAULT_SKOPEO_EXECUTABLE,
            command: list[str] = [],
            timeout: int = 60
        ) -> None:
        
        self.skopeo_executable: str = executable
        self.skopeo_command: list[str] = command
        
        self.timeout = timeout
    
        self.skopeo_execution: subprocess.CompletedProcess[bytes] = self.execute()

    def execute(self) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run([
            self.get_executable(),
            *self.get_command()
        ], capture_output=True, timeout=self.timeout)
    
    def get_executable(self) -> str:
        return self.skopeo_executable
    
    def get_command(self) -> list[str]:
        return self.skopeo_command

    def get_execution(self) -> subprocess.CompletedProcess[bytes]:
        return self.skopeo_execution

    def get_return_code(self) -> str:
        return self.get_execution().returncode

    def get_stdout(self) -> str:
        return self.get_execution().stdout

    def get_stderr(self) -> str:
        return self.get_execution().stderr

    def failed(self) -> bool:
        return self.get_return_code() != 0
    
    def success(self) -> bool:
        return self.get_return_code() == 0

    def __str__(self) -> str:
        return str({
            'return_code': self.get_return_code(),
            'stdout': self.get_stdout(),
            'stderr': self.get_stderr()
        })