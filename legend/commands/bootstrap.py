import subprocess
import sys
import platform
from typing import List, Dict, Optional
from .base import Command

class Dependency:
    def __init__(self, name: str, check_cmd: str, install_cmd: Optional[str] = None, 
                 check_output: Optional[str] = None, homepage: Optional[str] = None):
        self.name = name
        self.check_cmd = check_cmd
        self.install_cmd = install_cmd
        self.check_output = check_output  # If set, check if output contains this string
        self.homepage = homepage

class BootstrapCommand(Command):
    """Command to check and install dependencies"""

    def __init__(self):
        super().__init__(
            name='bootstrap',
            description='Check and install dependencies',
            aliases=[]
        )

    def get_dependencies(self) -> List[Dependency]:
        """Define all dependencies and how to check/install them"""
        return [
            Dependency(
                name="Homebrew",
                check_cmd="brew --version",
                homepage="https://brew.sh",
            ),
            Dependency(
                name="Git",
                check_cmd="git --version",
                homepage="https://git-scm.com",
            ),
            Dependency(
                name="pip",
                check_cmd="pip3 --version",
                install_cmd="python3 -m ensurepip --upgrade",
                homepage="https://pip.pypa.io",
            ),
            Dependency(
                name="Azure Functions Core Tools",
                check_cmd="func --version",
                install_cmd="brew install azure-functions-core-tools@4",
                homepage="https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local",
            ),
            Dependency(
                name="Azure CLI",
                check_cmd="az --version",
                install_cmd="brew install azure-cli",
                homepage="https://learn.microsoft.com/en-us/cli/azure/install-azure-cli",
            ),
        ]

    def check_dependency(self, dep: Dependency) -> bool:
        """Check if a dependency is installed"""
        try:
            result = self.run_subprocess(
                dep.check_cmd.split(),
                capture_output=True,
                check=False
            )
            if result is None:
                return False
            if dep.check_output:
                return dep.check_output in result.stdout
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def install_dependency(self, dep: Dependency) -> bool:
        """Install a dependency"""
        if not dep.install_cmd:
            return False
            
        result = self.run_subprocess(
            dep.install_cmd.split(),
            check=True,
            capture_output=True
        )
        return result is not None

    def handle(self, args):
        """Check for missing dependencies and offer to install them"""
        if platform.system() != "Darwin":
            self.error("This command currently only supports macOS")
            sys.exit(1)

        self.info("Checking dependencies...")
        missing: List[Dependency] = []
        installed: List[Dependency] = []
        
        for dep in self.get_dependencies():
            self.info(f"\nChecking {dep.name}...")
            if self.check_dependency(dep):
                self.success(f"{dep.name} is installed")
                installed.append(dep)
            else:
                self.error(f"{dep.name} is not installed")
                missing.append(dep)
        
        if not missing:
            print("\n")
            self.completed("All dependencies are installed!")
            return
        
        self.info("\nMissing dependencies:")
        for dep in missing:
            self.info(f"\n{dep.name}:")
            if dep.install_cmd:
                self.info(f"  To install: {dep.install_cmd}")
                response = input(f"  Would you like to install {dep.name} now? [y/N] ")
                if response.lower() == 'y':
                    self.info(f"\nInstalling {dep.name}...")
                    if self.install_dependency(dep):
                        self.success(f"{dep.name} installed successfully")
                    else:
                        self.error(f"Failed to install {dep.name}")
                        if dep.homepage:
                            self.info(f"Please install manually: {dep.homepage}")
            else:
                self.info("  Please install manually:")
                if dep.homepage:
                    self.info(f"  {dep.homepage}")
