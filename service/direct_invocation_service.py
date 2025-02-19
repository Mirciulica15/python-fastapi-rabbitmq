import subprocess


class DirectInvocationService:
    """Service for directly invoking a PowerShell cmdlet and capturing the output."""

    def __init__(self, cmdlet: str):
        self.cmdlet = cmdlet

    def execute_cmdlet(self) -> str:
        """Execute the PowerShell cmdlet and capture the output."""
        try:
            result = subprocess.run(
                ["powershell", "-Command", self.cmdlet],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Result of Cmdlet execution: {result.stdout.strip()}")
            return result.stdout.strip()

        except subprocess.CalledProcessError as e:
            print(f"Error executing cmdlet: {e}")
            return f"Error: {e}"
