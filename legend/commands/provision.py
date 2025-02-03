from .base import Command

class ProvisionCommand(Command):
    """Command to provision Azure resources for the application"""

    def __init__(self):
        super().__init__(
            name='provision',
            description='Provision Azure resources for the application',
            aliases=['p']
        )

    def add_arguments(self, parser):
        parser.add_argument('environment', 
                          help='Environment to provision (e.g., development, test, sit)')


    def handle(self, args):
        # - load config
        self.load_config(args.environment)
        env = args.environment

        # - configure file names from config
        deployment_template = f"deployment/azuredeploy-{ env }.json"
        parameters = f"deployment/azuredeploy-{ env }.parameters.json"
        
        # create resource group (safe to do even if already exists)
        self.run_azure_command(
            [
                "az",
                "group",
                "create",
                "--name", self.config.azure.resource_group,
                "--location", self.config.azure.location
            ]
        )

        # provision resources using ARM templates in deployment
        try:
            self.run_subprocess(
                [
                    "az",
                    "deployment",
                    "group",
                    "create",
                    "--name", f"{self.config.settings.app_name}-{ env }", # FIXME: get this from config?
                "--resource-group", self.config.azure.resource_group,
                "--template-file", f"deployment/azuredeploy-{ env }.json",
                "--parameters", f"@deployment/azuredeploy-{ env }.parameters.json"
                ],
                check=True,
                capture_output=False
            )
        except Exception as e:
            if self.verbose:
                print(e)
            return    

