# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest  # pylint: disable=unused-import

from azure.cli.testsdk import (ResourceGroupPreparer)
from azure.cli.testsdk.decorators import serial_test
from azext_containerapp_compose.tests.latest.common import (ContainerappComposePreviewScenarioTest,  # pylint: disable=unused-import
                                                            write_test_file,
                                                            clean_up_test_file,
                                                            TEST_DIR)


class ContainerappComposeLocationScenarioTest(ContainerappComposePreviewScenarioTest):

    @serial_test()
    @ResourceGroupPreparer(name_prefix='cli_test_containerapp_preview', location='eastus')
    def test_containerapp_compose_create_location_differ_from_resource_group(self, resource_group):
        compose_text = """
services:
  foo:
    image: smurawski/printenv:latest
"""
        compose_file_name = f"{self._testMethodName}_compose.yml"
        write_test_file(compose_file_name, compose_text)

        self.kwargs.update({
            'environment': self.create_random_name(prefix='containerapp-compose', length=24),
            'workspace': self.create_random_name(prefix='containerapp-compose', length=24),
            'compose': compose_file_name,
            'location': 'canadacentral',
        })

        command_string = 'containerapp compose create'
        command_string += ' --compose-file-path {compose}'
        command_string += ' --resource-group {rg}'
        command_string += ' --environment {environment}'
        command_string += ' --logs-workspace {workspace}'
        command_string += ' --location {location}'
        self.cmd(command_string, checks=[
            self.check('[].location', ['Canada Central']),
            self.check('[] | length(@)', 1),
        ])

        clean_up_test_file(compose_file_name)
