# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

"""
Test class for Activation key CLI
"""

from ddt import ddt
from nose.plugins.attrib import attr

from robottelo.cli.activationkey import ActivationKey
from robottelo.cli.lifecycleenvironment import LifecycleEnvironment
from robottelo.cli.factory import (
    make_activation_key,
    make_lifecycle_environment,
    make_org, make_product
)
from robottelo.common.decorators import data, stubbed
from robottelo.common.helpers import generate_string

from tests.foreman.cli.basecli import BaseCLI


@ddt
class TestActivationKey(BaseCLI):
    """
    Activation Key CLI tests
    """

    org = None
    library = None
    product = None
    env1 = None
    env2 = None

    def setUp(self):
        """
        Tests for activation keys via Hammer CLI
        """

        super(TestActivationKey, self).setUp()

        if TestActivationKey.org is None:
            TestActivationKey.org = make_org()
        if TestActivationKey.env1 is None:
            TestActivationKey.env1 = make_lifecycle_environment(
                {u'organization-id': TestActivationKey.org['id']})
        if TestActivationKey.env2 is None:
            TestActivationKey.env2 = make_lifecycle_environment(
                {u'organization-id': TestActivationKey.org['id'],
                 u'prior': TestActivationKey.env1['label']})
        if TestActivationKey.product is None:
            TestActivationKey.product = make_product(
                {u'organization-id': TestActivationKey.org['id']})

        if TestActivationKey.library is None:
            TestActivationKey.library = LifecycleEnvironment.info(
                {'organization-id': TestActivationKey.org['id'],
                 'name': 'Library'}).stdout

    def _make_activation_key(self, options=None):
        """ Make a new activation key and assert its success"""

        if options is None:
            options = {}

        # Use default organization if None are provided
        if (
                not options.get('organization', None)
                and not options.get('organization-label', None)
                and not options.get('organization-id', None)):
            options['organization-id'] = self.org['id']

        # Create activation key
        ackey = make_activation_key(options)

        # Fetch it
        result = ActivationKey.info(
            {
                'id': ackey['id']
            }
        )

        self.assertEqual(
            result.return_code,
            0,
            "Activation key was not found: %s" % str(result.stderr))
        self.assertEqual(
            len(result.stderr),
            0,
            "No error was expected %s" % str(result.stderr))

        # Return the activation key dictionary
        return ackey

    @data(
        {'name': generate_string('alpha', 15)},
        {'name': generate_string('alphanumeric', 15)},
        {'name': generate_string('numeric', 15)},
        {'name': generate_string('latin1', 15)},
        {'name': generate_string('utf8', 15)},
        {'name': generate_string('html', 15)},
    )
    @attr('cli', 'activation-key')
    def test_positive_create_activation_key_1(self, test_data):
        """
        @Test: Create Activation key for all variations of Activation key name
        @Feature: Activation key
        @Steps:
        1. Create Activation key for all valid Activation Key name variation
        @Assert: Activation key is created with chosen name
        """

        new_ackey = self._make_activation_key({u'name': test_data['name']})
        # Name should match passed data
        self.assertEqual(
            new_ackey['name'],
            test_data['name'],
            ("Names don't match: '%s' != '%s'" %
             (new_ackey['name'], test_data['name']))
        )

    @data(
        {'description': generate_string('alpha', 15)},
        {'description': generate_string('alphanumeric', 15)},
        {'description': generate_string('numeric', 15)},
        {'description': generate_string('latin1', 15)},
        {'description': generate_string('utf8', 15)},
        {'description': generate_string('html', 15)},
    )
    @attr('cli', 'activation-key')
    def test_positive_create_activation_key_2(self, test_data):
        """
        @Test: Create Activation key for all variations of Description
        @Feature: Activation key
        @Steps:
        1. Create Activation key for all valid Description variation
        @Assert: Activation key is created with chosen description
        """

        new_ackey = self._make_activation_key(
            {u'description': test_data['description']})
        # Description should match passed data
        self.assertEqual(
            new_ackey['description'],
            test_data['description'],
            ("Descriptions don't match: '%s' != '%s'" %
             (new_ackey['description'], test_data['description']))
        )

    @data(
        {'name': generate_string('alpha', 15)},
        {'name': generate_string('alphanumeric', 15)},
        {'name': generate_string('numeric', 15)},
        {'name': generate_string('latin1', 15)},
        {'name': generate_string('utf8', 15)},
        {'name': generate_string('html', 15)},
    )
    @attr('cli', 'activation-key')
    def test_positive_create_associate_environ_1(self, test_data):
        """
        @Test: Create Activation key and associate with Library environment
        @Feature: Activation key
        @Steps:
        1. Create Activation key for variations of Name / associated to Library
        @Assert: Activation key is created and associated to Library
        @Status: Manual
        """

        new_ackey = self._make_activation_key(
            {u'name': test_data['name'],
             u'environment-id': self.library['id']})
        # Description should match passed data
        self.assertEqual(
            new_ackey['lifecycle-environment'],
            self.library['name'],
            ("Environments don't match: '%s' != '%s'" %
             (new_ackey['lifecycle-environment'], self.library['name']))
        )

    @data(
        {'name': generate_string('alpha', 15)},
        {'name': generate_string('alphanumeric', 15)},
        {'name': generate_string('numeric', 15)},
        {'name': generate_string('latin1', 15)},
        {'name': generate_string('utf8', 15)},
        {'name': generate_string('html', 15)},
    )
    @attr('cli', 'activation-key')
    def test_positive_create_associate_environ_2(self, test_data):
        """
        @Test: Create Activation key and associate with environment
        @Feature: Activation key
        @Steps:
        1. Create Activation key for variations of Name / associated to environ
        @Assert: Activation key is created and associated to environment
        @Status: Manual
        """

        new_ackey = self._make_activation_key(
            {u'name': test_data['name'],
             u'environment-id': self.env1['id']})
        # Description should match passed data
        self.assertEqual(
            new_ackey['lifecycle-environment'],
            self.env1['name'],
            ("Environments don't match: '%s' != '%s'" %
             (new_ackey['lifecycle-environment'], self.env1['name']))
        )

    @stubbed
    def test_positive_create_activation_key_4(self):
        """
        @Feature: Activation key - Positive Create
        @Test: Create Activation key for all variations of Content Views
        @Steps:
        1. Create Activation key for all valid Content views in [1]
        using valid Name, Description, Environment and Usage limit
        @Assert: Activation key is created
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_create_activation_key_5(self):
        """
        @Feature: Activation key - Positive Create
        @Test: Create Activation key for all variations of System Groups
        @Steps:
        1. Create Activation key for all valid System Groups in [1]
        using valid Name, Description, Environment, Content View, Usage limit
        @Assert: Activation key is created
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_create_activation_key_6(self):
        """
        @Feature: Activation key - Positive Create
        @Test: Create Activation key with default Usage limit (Unlimited)
        @Steps:
        1. Create Activation key with default Usage Limit (Unlimited)
        using valid Name, Description, Environment and Content View
        @Assert: Activation key is created
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_create_activation_key_7(self):
        """
        @Feature: Activation key - Positive Create
        @Test: Create Activation key with finite Usage limit
        @Steps:
        1. Create Activation key with finite Usage Limit (Not Unlimited)
        using valid Name, Description, Environment and Content View
        @Assert: Activation key is created
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_create_activation_key_8(self):
        """
        @Feature: Activation key - Positive Create
        @Test: Create Activation key with minimal input parameters
        @Steps:
        1. Create Activation key by entering Activation Key Name alone
        leaving Description, Content View and Usage Limit as default values
        @Assert: Activation key is created
        @Status: Manual
        """
        pass

    @stubbed
    def test_negative_create_activation_key_1(self):
        """
        @Feature: Activation key - Negative Create
        @Test: Create Activation key with invalid Name
        @Steps:
        1. Create Activation key for all invalid Activation Key Names in [2]
        using valid Description, Environment, Content View, Usage limit
        @Assert: Activation key is not created. Appropriate error shown.
        @Status: Manual
        """
        pass

    @stubbed
    def test_negative_create_activation_key_2(self):
        """
        @Feature: Activation key - Negative Create
        @Test: Create Activation key with invalid Description
        @Steps:
        1. Create Activation key for all invalid Description in [2]
        using valid Name, Environment, Content View, Usage limit
        @Assert: Activation key is not created. Appropriate error shown.
        @Status: Manual
        """
        pass

    @stubbed
    def test_negative_create_activation_key_3(self):
        """
        @Feature: Activation key - Negative Create
        @Test: Create Activation key with invalid Usage Limit
        @Steps:
        1. Create Activation key for all invalid Usage Limit in [2]
        using valid Name, Description, Environment, Content View
        @Assert: Activation key is not created. Appropriate error shown.
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_delete_activation_key_1(self):
        """
        @Feature: Activation key - Positive Delete
        @Test: Create Activation key and delete it for all variations of
        Activation key name
        @Steps:
        1. Create Activation key for all valid Activation Key names in [1]
        using valid Description, Environment, Content View, Usage limit
        2. Delete the Activation key
        @Assert: Activation key is deleted
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_delete_activation_key_2(self):
        """
        @Feature: Activation key - Positive Delete
        @Test: Create Activation key and delete it for all variations of
        Description
        @Steps:
        1. Create Activation key for all valid Description in [1]
        using valid Name, Environment, Content View, Usage limit
        2. Delete the Activation key
        @Assert: Activation key is deleted
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_delete_activation_key_3(self):
        """
        @Feature: Activation key - Positive Delete
        @Test: Create Activation key and delete it for all variations of
        Environment
        @Steps:
        1. Create Activation key for all valid Environments in [1]
        using valid Name, Description, Content View, Usage limit
        2. Delete the Activation key
        @Assert: Activation key is deleted
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_delete_activation_key_4(self):
        """
        @Feature: Activation key - Positive Delete
        @Test: Create Activation key and delete it for all variations of
        Content Views
        @Steps:
        1. Create Activation key for all valid Content Views in [1]
        using valid Name, Description, Environment, Usage limit
        2. Delete the Activation key
        @Assert: Activation key is deleted
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_delete_activation_key_5(self):
        """
        @Feature: Activation key - Positive Delete
        @Test: Delete an Activation key which has registered systems
        @Steps:
        1. Create an Activation key
        2. Register systems to it
        3. Delete the Activation key
        @Assert: Activation key is deleted
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_delete_activation_key_6(self):
        """
        @Feature: Activation key - Positive Delete
        @Test: Delete a Content View associated to an Activation Key deletes
        the Activation Key
        @Steps:
        1. Create an Activation key with a Content View
        2. Delete the Content View
        @Assert: Activation key is deleted or updated accordingly
        @Status: Manual
        """
        pass

    @stubbed
    def test_negative_delete_activation_key_1(self):
        """
        @Feature: Activation key - Positive Delete
        @Test: [UI ONLY] Attempt to delete an Activation Key and cancel it
        @Steps:
        1. Create an Activation key
        2. Attempt to remove an Activation Key
        3. Click Cancel in the confirmation dialog box
        @Assert: Activation key is not deleted
        @Status: Manual
        """
        pass  # Skip for CLI as this is UI only

    @stubbed
    def test_positive_update_activation_key_1(self):
        """
        @Feature: Activation key - Positive Update
        @Test: Update Activation Key Name in an Activation key
        @Steps:
        1. Create Activation key
        2. Update Activation key name for all variations in [1]
        @Assert: Activation key is updated
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_update_activation_key_2(self):
        """
        @Feature: Activation key - Positive Update
        @Test: Update Description in an Activation key
        @Steps:
        1. Create Activation key
        2. Update Description for all variations in [1]
        @Assert: Activation key is updated
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_update_activation_key_3(self):
        """
        @Feature: Activation key - Positive Update
        @Test: Update Environment in an Activation key
        @Steps:
        1. Create Activation key
        2. Update Environment for all variations in [1]
        @Assert: Activation key is updated
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_update_activation_key_4(self):
        """
        @Feature: Activation key - Positive Update
        @Test: Update Content View in an Activation key
        @Steps:
        1. Create Activation key
        2. Update Content View for all variations in [1] and include both
        RH and custom products
        @Assert: Activation key is updated
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_update_activation_key_5(self):
        """
        @Feature: Activation key - Positive Update
        @Test: Update Usage limit from Unlimited to a finite number
        @Steps:
        1. Create Activation key
        2. Update Usage limit from Unlimited to a definite number
        @Assert: Activation key is updated
        @Status: Manual
        """
        pass

    @stubbed
    def test_positive_update_activation_key_6(self):
        """
        @Feature: Activation key - Positive Update
        @Test: Update Usage limit from definite number to Unlimited
        @Steps:
        1. Create Activation key
        2. Update Usage limit from definite number to Unlimited
        @Assert: Activation key is updated
        @Status: Manual
        """
        pass

    @stubbed
    def test_negative_update_activation_key_1(self):
        """
        @Feature: Activation key - Negative Update
        @Test: Update invalid name in an activation key
        @Steps:
        1. Create Activation key
        2. Update Activation key name for all variations in [2]
        @Assert: Activation key is not updated.  Appropriate error shown.
        @Status: Manual
        """
        pass

    @stubbed
    def test_negative_update_activation_key_2(self):
        """
        @Feature: Activation key - Negative Update
        @Test: Update invalid Description in an activation key
        @Steps:
        1. Create Activation key
        2. Update Description for all variations in [2]
        @Assert: Activation key is not updated.  Appropriate error shown.
        @Status: Manual
        """
        pass

    @stubbed
    def test_negative_update_activation_key_3(self):
        """
        @Feature: Activation key - Negative Update
        @Test: Update invalid Usage Limit in an activation key
        @Steps:
        1. Create Activation key
        2. Update Usage Limit for all variations in [2]
        @Assert: Activation key is not updated.  Appropriate error shown.
        @Status: Manual
        """
        pass

    @stubbed
    def test_usage_limit(self):
        """
        @Feature: Activation key - Usage limit
        @Test: Test that Usage limit actually limits usage
        @Steps:
        1. Create Activation key
        2. Update Usage Limit to a finite number
        3. Register Systems to match the Usage Limit
        4. Attempt to register an other system after reaching the Usage Limit
        @Assert: System Registration fails. Appropriate error shown
        @Status: Manual
        """
        pass

    @stubbed
    def test_associate_host(self):
        """
        @Feature: Activation key - Host
        @Test: Test that hosts can be associated to Activation Keys
        @Steps:
        1. Create Activation key
        2. Create different hosts
        3. Associate the hosts to Activation key
        @Assert: Hosts are successfully associated to Activation key
        @Status: Manual
        """
        pass

    @stubbed
    def test_associate_product_1(self):
        """
        @Feature: Activation key - Product
        @Test: Test that RH product can be associated to Activation Keys
        @Steps:
        1. Create Activation key
        2. Associate RH product(s) to Activation Key
        @Assert: RH products are successfully associated to Activation key
        @Status: Manual
        """
        pass

    @stubbed
    def test_associate_product_2(self):
        """
        @Feature: Activation key - Product
        @Test: Test that custom product can be associated to Activation Keys
        @Steps:
        1. Create Activation key
        2. Associate custom product(s) to Activation Key
        @Assert: Custom products are successfully associated to Activation key
        @Status: Manual
        """
        pass

    @stubbed
    def test_associate_product_3(self):
        """
        @Feature: Activation key - Product
        @Test: Test that RH/Custom product can be associated to Activation keys
        @Steps:
        1. Create Activation key
        2. Associate RH product(s) to Activation Key
        3. Associate custom product(s) to Activation Key
        @Assert: RH/Custom product is successfully associated to Activation key
        @Status: Manual
        """
        pass

    @stubbed
    def test_delete_manifest(self):
        """
        @Feature: Activation key - Manifest
        @Test: Check if deleting a manifest removes it from Activation key
        @Steps:
        1. Create Activation key
        2. Associate a manifest to the Activation Key
        3. Delete the manifest
        @Assert: Deleting a manifest removes it from the Activation key
        @Status: Manual
        """
        pass

    @stubbed
    def test_multiple_activation_keys_to_system(self):
        """
        @Feature: Activation key - System
        @Test: Check if multiple Activation keys can be attached to a system
        @Steps:
        1. Create multiple Activation keys
        2. Attach all the created Activation keys to a System
        @Assert: Multiple Activation keys are attached to a system
        @Status: Manual
        """
        pass

    @stubbed
    def test_list_activation_keys_1(self):
        """
        @Feature: Activation key - list
        @Test: List Activation key for all variations of Activation key name
        @Steps:
        1. Create Activation key for all valid Activation Key name variation
        in [1]
        2. List Activation key
        @Assert: Activation key is listed
        @Status: Manual
        """
        pass

    @stubbed
    def test_list_activation_keys_2(self):
        """
        @Feature: Activation key - list
        @Test: List Activation key for all variations of Description
        @Steps:
        1. Create Activation key for all valid Description variation in [1]
        2. List Activation key
        @Assert: Activation key is listed
        @Status: Manual
        """
        pass

    @stubbed
    def test_search_activation_keys_1(self):
        """
        @Feature: Activation key - search
        @Test: Search Activation key for all variations of Activation key name
        @Steps:
        1. Create Activation key for all valid Activation Key name variation
        in [1]
        2. Search/find Activation key
        @Assert: Activation key is found
        @Status: Manual
        """
        pass

    @stubbed
    def test_search_activation_keys_2(self):
        """
        @Feature: Activation key - search
        @Test: Search Activation key for all variations of Description
        @Steps:
        1. Create Activation key for all valid Description variation in [1]
        2. Search/find Activation key
        @Assert: Activation key is found
        @Status: Manual
        """
        pass

    @stubbed
    def test_info_activation_keys_1(self):
        """
        @Feature: Activation key - info
        @Test: Get Activation key info for all variations of Activation key
        name
        @Steps:
        1. Create Activation key for all valid Activation Key name variation
        in [1]
        2. Get info of the Activation key
        @Assert: Activation key info is displayed
        @Status: Manual
        """
        pass

    @stubbed
    def test_info_activation_keys_2(self):
        """
        @Feature: Activation key - info
        @Test: Get Activation key info for all variations of Description
        @Steps:
        1. Create Activation key for all valid Description variation in [1]
        2. Get info of the Activation key
        @Assert: Activation key info is displayed
        @Status: Manual
        """
        pass

    @stubbed
    def test_end_to_end(self):
        """
        @Feature: Activation key - End to End
        @Test: Create Activation key and provision systems with it
        @Steps:
        1. Create Activation key
        2. Provision systems with Activation key
        @Assert: Systems are successfully provisioned with Activation key
        @Status: Manual
        """
        pass
