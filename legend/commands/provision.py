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
        parser.add_argument('--shared-resources', '-shared',
                          action='store_true',
                          help='Only provision shared resources such as log analytics')

    def provision_shared(self, args) -> str:
        shared_resource_group_name = f"legend-shared-resources-{ self.config.azure.location }"

        # create resource group for shared resources such as analytics
        self.run_azure_command(
            [
                "az",
                "group",
                "create",
                "--name", shared_resource_group_name,
                "--location", self.config.azure.location
            ]
        )

        # create shared log analytics workspace
        analytics = self.run_azure_command(
            [
                "az",
                "monitor",
                "log-analytics",
                "workspace",
                "create",
                "--resource-group", shared_resource_group_name,
                "--workspace-name", f"legend-log-analytics-{ self.config.azure.location }",
                "--location", self.config.azure.location
            ]
        )
        # extract id and return it
        return analytics["id"]      

    def provision_app(self, args, shared_workspace_id):
        env = args.environment

        # - configure file names from config
        deployment_template = f"deployment/azuredeploy-{ env }.json"
        parameters = f"deployment/azuredeploy-{ env }.parameters.json"
        
        # create resource group for the app (safe to do even if already exists)
        self.run_azure_command(
            [
                "az",
                "group",
                "create",
                "--name", self.config.azure.resource_group,
                "--location", self.config.azure.location
            ]
        )

        # provision resources using ARM templates in deployment folder
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
                    "--parameters", f"@deployment/azuredeploy-{ env }.parameters.json", f"logAnalyticsWorkspaceName={shared_workspace_id}"
                ],
                check=True,
                capture_output=False
            )
        except Exception as e:
            if self.verbose:
                print(e)
            return

    def handle(self, args):
        # Load config
        self.load_config(args.environment)        

        shared_workspace_id = self.provision_shared(args)

        if not args.shared_resources:
            self.provision_app(args, shared_workspace_id)


