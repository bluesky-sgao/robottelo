import unittest

from robottelo.common.helpers import (
    generate_name, generate_email_address, valid_names_list, valid_data_list,
    invalid_names_list, generate_ipaddr, generate_mac, generate_string,
    generate_strings_list, escape_search, info_dictionary)


class FakeSSHResult(object):
    def __init__(self, stdout=None):
        self.stdout = stdout


class GenerateNameTestCase(unittest.TestCase):
    def test_return_type(self):
        """Tests if generate name returns a unicode string"""
        self.assertIsInstance(generate_name(), unicode)


class GenerateEmailAddressTestCase(unittest.TestCase):
    def test_return_type(self):
        """Tests if generate email address returns a unicode string"""
        self.assertIsInstance(generate_email_address(), unicode)


class ValidNamesListTestCase(unittest.TestCase):
    def test_return_type(self):
        """Tests if valid names list returns a unicode string"""
        for name in valid_names_list():
            self.assertIsInstance(name, unicode)


class ValidDataListTestCase(unittest.TestCase):
    def test_return_type(self):
        """Tests if valid data list returns a unicode string"""
        for data in valid_data_list():
            self.assertIsInstance(data, unicode)


class InvalidNamesListTestCase(unittest.TestCase):
    def test_return_type(self):
        """Tests if invalid names list returns a unicode string"""
        for name in invalid_names_list():
            self.assertIsInstance(name, unicode)


class GenerateIPAddrTestCase(unittest.TestCase):
    def test_return_type(self):
        """Tests if generate ipaddr returns a unicode string"""
        self.assertIsInstance(generate_ipaddr(), unicode)
        self.assertIsInstance(generate_ipaddr(ip3=True), unicode)


class GenerateMACTestCase(unittest.TestCase):
    def test_return_type(self):
        """Tests if generate mac returns a unicode string"""
        self.assertIsInstance(generate_mac(), unicode)


class GenerateStringTestCase(unittest.TestCase):
    def test_alphanumeric_return_type(self):
        """Tests if generate alphanumeric string returns a unicode string"""
        self.assertIsInstance(generate_string('alphanumeric', 8), unicode)

    def test_alpha_return_type(self):
        """Tests if generate alpha string returns a unicode string"""
        self.assertIsInstance(generate_string('alpha', 8), unicode)

    def test_numeric_return_type(self):
        """Tests if generate numeric string returns a unicode string"""
        self.assertIsInstance(generate_string('numeric', 8), unicode)

    def test_latin1_return_type(self):
        """Tests if generate latin1 string returns a unicode string"""
        self.assertIsInstance(generate_string('latin1', 8), unicode)

    def test_utf8_return_type(self):
        """Tests if generate utf-8 string returns a unicode string"""
        self.assertIsInstance(generate_string('utf8', 8), unicode)

    def test_html_return_type(self):
        """Tests if generate html string returns a unicode string"""
        self.assertIsInstance(generate_string('html', 8), unicode)


class GenerateStringListTestCase(unittest.TestCase):
    def test_return_type(self):
        """Tests if generate string list returns a unicode string"""
        for string in generate_strings_list():
            self.assertIsInstance(string, unicode)


class EscapeSearchTestCase(unittest.TestCase):
    def test_return_type(self):
        """Tests if escape search returns a unicode string"""
        self.assertIsInstance(escape_search('search term'), unicode)

    def test_escapes_double_quotes(self):
        """Tests if escape search escapes double quotes"""
        self.assertEqual(escape_search('termwith"')[1:-1], 'termwith\\"')

    def test_escapes_backslash(self):
        """Tests if escape search escapes backslashes"""
        self.assertEqual(escape_search('termwith\\')[1:-1], 'termwith\\\\')

    def test_escapes_double_quotes_and_backslash(self):
        """Tests if escape search escapes backslashes"""
        self.assertEqual(escape_search('termwith"and\\')[1:-1],
                         'termwith\\"and\\\\')

    def test_wraps_in_double_quotes(self):
        """Tests if escape search wraps the term in double quotes"""
        term = escape_search('term')
        self.assertEqual(term[0], '"')
        self.assertEqual(term[-1], '"')


class InfoDictionaryTestCase(unittest.TestCase):
    def test_parse_simple(self):
        """Can parse a simple info output"""
        output = FakeSSHResult(stdout=[
            'Id:                 19',
            'Full name:          4iv01o2u 10.5',
            'Release name:',
            '',
            'Family:',
            'Name:               4iv01o2u',
            'Major version:      10',
            'Minor version:      5',
        ])

        result = info_dictionary(output)
        self.assertDictEqual(result.stdout, {
            'id': '19',
            'full-name': '4iv01o2u 10.5',
            'release-name': {},
            'family': {},
            'name': '4iv01o2u',
            'major-version': '10',
            'minor-version': '5',
        })

    def test_parse_numbered_list_attributes(self):
        """Can parse numbered list attributes"""
        output = FakeSSHResult(stdout=[
            'Partition tables:',
            ' 1) ptable1',
            ' 2) ptable2',
            ' 3) ptable3',
            ' 4) ptable4',
        ])

        result = info_dictionary(output)
        self.assertDictEqual(result.stdout, {
            'partition-tables': [
                'ptable1',
                'ptable2',
                'ptable3',
                'ptable4',
            ],
        })

    def test_parse_list_attributes(self):
        """Can parse list attributes"""
        output = FakeSSHResult(stdout=[
            'Partition tables:',
            ' ptable1',
            ' ptable2',
            ' ptable3',
            ' ptable4',
        ])

        result = info_dictionary(output)
        self.assertDictEqual(result.stdout, {
            'partition-tables': [
                'ptable1',
                'ptable2',
                'ptable3',
                'ptable4',
            ],
        })

    def test_parse_dict_attributes(self):
        """Can parse dict attributes"""
        output = FakeSSHResult(stdout=[
            'Content:',
            ' 1) Repo Name: repo1',
            '    URL:       /custom/url1',
            ' 2) Repo Name: repo2',
            '    URL:       /custom/url2',
        ])

        result = info_dictionary(output)
        self.assertDictEqual(result.stdout, {
            'content': [{
                'repo-name': 'repo1',
                'url': '/custom/url1',
            }, {
                'repo-name': 'repo2',
                'url': '/custom/url2',
            }],
        })
