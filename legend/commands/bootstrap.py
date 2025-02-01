import subprocess
import sys
import platform
from typing import List, Dict, Optional

class Dependency:
    def __init__(self, name: str, check_cmd: str, install_cmd: Optional[str] = None, 
                 check_output: Optional[str] = None, homepage: Optional[str] = None):
        self.name = name
        self.check_cmd = check_cmd
        self.install_cmd = install_cmd
        self.check_output = check_output  # If set, check if output contains this string
        self.homepage = homepage

def get_dependencies() -> List[Dependency]:
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

def check_dependency(dep: Dependency) -> bool:
    """Check if a dependency is installed"""
    try:
        result = subprocess.run(
            dep.check_cmd.split(),
            capture_output=True,
            text=True
        )
        if dep.check_output:
            return dep.check_output in result.stdout
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_dependency(dep: Dependency) -> bool:
    """Install a dependency"""
    if not dep.install_cmd:
        return False
        
    try:
        subprocess.run(dep.install_cmd.split(), check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def run(args):
    """Check for missing dependencies and offer to install them"""
    if platform.system() != "Darwin":
        print("⛔️ Error: This command currently only supports macOS")
        sys.exit(1)

    print("Checking dependencies...")
    missing: List[Dependency] = []
    installed: List[Dependency] = []
    
    for dep in get_dependencies():
        print(f"\nChecking {dep.name}...")
        if check_dependency(dep):
            print(f"✅ {dep.name} is installed")
            installed.append(dep)
        else:
            print(f"❌ {dep.name} is not installed")
            missing.append(dep)
    
    if not missing:
        print("\n✨ All dependencies are installed!")
        return
    
    print("\nMissing dependencies:")
    for dep in missing:
        print(f"\n{dep.name}:")
        if dep.install_cmd:
            print(f"  To install: {dep.install_cmd}")
            response = input(f"  Would you like to install {dep.name} now? [y/N] ")
            if response.lower() == 'y':
                print(f"\nInstalling {dep.name}...")
                if install_dependency(dep):
                    print(f"✅ {dep.name} installed successfully")
                else:
                    print(f"⛔️ Failed to install {dep.name}")
                    if dep.homepage:
                        print(f"Please install manually: {dep.homepage}")
        else:
            print("  Please install manually:")
            if dep.homepage:
                print(f"  {dep.homepage}")
