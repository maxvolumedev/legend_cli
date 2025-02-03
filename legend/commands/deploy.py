import re
from pathlib import Path
from subprocess import STDOUT
from .base import Command


def clean_git_url(url: str) -> str:
    """Remove any credentials from git URL"""
    return re.sub(r'https://[^@]*@', 'https://', url)


class DeployCommand(Command):
    """Deploy function app to Azure"""

    def __init__(self):
        super().__init__(
            name='deploy',
            description='Deploy function app to Azure'
        )

    def add_arguments(self, parser):
        parser.add_argument('environment',
                          help='Environment to deploy to (e.g., development, test, sit)')

    def git_branches_identical(self, branch1: str, branch2: str) -> bool:
        """Check if two git branches have identical content.
        Returns True if branches are identical, False if there are differences."""
        self.info(f"Checking if {branch1} matches {branch2}...")
        
        # First ensure both branches exist
        for branch in [branch1, branch2]:
            result = self.run_subprocess(["git", "rev-parse", "--verify", branch], check=False)
            if result is None:
                self.error(f"Branch '{branch}' does not exist")
                return False
        
        # Compare the branches using git diff
        result = self.run_subprocess(["git", "diff", "--quiet", f"{branch1}..{branch2}"], check=False)
        
        # git diff returns:
        # - 0 (success) if branches are identical
        # - 1 if there are differences
        # - other codes for errors
        if result is None:
            self.error(f"Failed to compare branches {branch1} and {branch2}")
            return False
            
        if result.returncode == 0:
            self.success(f"Branches {branch1} and {branch2} are identical")
            return True
        elif result.returncode == 1:
            self.warning(f"Found differences between {branch1} and {branch2}")
            # Show a summary of differences
            diff_stat = self.run_subprocess(["git", "diff", "--stat", f"{branch1}..{branch2}"], check=False)
            if diff_stat and diff_stat.stdout:
                self.info("\nChanges:")
                self.info(diff_stat.stdout)
            return False
        else:
            self.error(f"Error comparing branches: git diff returned {result.returncode}")
            return False

    def get_git_branch(self) -> str:
        """Returns current git branch."""
        self.info(f"Checking if current branch matches {self.config.azure.branch}...")
        
        result = self.run_subprocess(["git", "rev-parse", "--abbrev-ref", "HEAD"], check=False)
        if result is None:
            self.warning("Failed to get current git branch")
            return False
            
        return result.stdout.strip()


    def check_git_status(self) -> bool:
        """Check if there are any uncommitted changes in git.
        Returns True if working directory is clean, False if there are uncommitted changes."""
        self.info("Checking for uncommitted changes...")
        
        result = self.run_subprocess(["git", "status", "--porcelain"])
        if result is None:
            self.warning("Failed to check git status")
            return False
            
        if result.stdout.strip():
            self.warning("You have uncommitted changes. You should commit or stash them before deploying.")
            return False
            
        self.success("Working directory is clean")
        return True


    def handle(self, args):
        if not self.validate_environment(args.environment):
            return

        # Load configuration
        if not self.load_config(args.environment):
            return

        status = True

        # Safeguards:
        # 1. check if there are uncommitted changes in git
        status &= self.check_git_status()

        # 2. check if the current git branch matches config.azure.branch
        git_branch = self.get_git_branch()
        status &= git_branch == self.config.azure.branch

        # 3. if env is production, also check that current branch has no changes to uat branch
        if args.environment == "production":
            status &= self.git_branches_identical(git_branch, "uat") # TODO: make uat branch configurable?

        if not status:
            # Print helpful message and ask for y/N confirmation before deploying
            self.warning("There are potential issues with your deployment, see output above..")
            confirm = input("Are you sure you want to proceed? (y/N): ")
            if confirm.lower() != 'y':                    
                return


        if args.environment == "production":        
            # if not git_branch_ok, ask user to confirm deployment by typing the current branch name as confirmation
            if not git_branch_ok:
                print("\nTo deploy to production, current branch should be the same as config.azure.branch")
                confirm = input(f"Please type the current branch name ({ git_branch }): ")
                if confirm.lower() != git_branch:
                    return


        # call azure cli: func azure functionapp publish test3-sit
        try:
            self.run_subprocess(
                [
                    "func",
                    "azure",
                    "functionapp",
                    "publish",
                    self.config.azure.function_app # FIXME: need to make sure this is synced with our JSON deployment params
                ],
                check=True,
                capture_output=False
            )
        except Exception as e:            
            return

        self.completed(f"Successfully deployed to {args.environment}!")
