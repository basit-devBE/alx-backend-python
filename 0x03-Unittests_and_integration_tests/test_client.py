#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
import requests
from client import GithubOrgClient
from fixtures import (
    org_payload, 
    repos_payload, 
    expected_repos, 
    apache2_repos
)

class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.GithubOrgClient.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test the org method of GithubOrgClient
        
        Args:
            org_name (str): Name of the organization to test
            mock_get_json (MagicMock): Mocked get_json method
        """
        # Create an instance of GithubOrgClient with the org name
        gh_client = GithubOrgClient(org_name)
        
        # Call the org property
        gh_client.org
        
        # Assert that get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """
        Test the _public_repos_url property
        """
        # Payload to mock the org method
        test_payload = {"repos_url": "https://api.github.com/orgs/test-org/repos"}
        
        # Use patch as a context manager to mock the org property
        with patch('client.GithubOrgClient.org', 
                   new_callable=PropertyMock,
                   return_value=test_payload) as mock_org:
            # Create client instance
            gh_client = GithubOrgClient("test-org")
            
            # Get the public repos URL
            result = gh_client._public_repos_url
            
            # Check the result matches the mocked payload
            self.assertEqual(result, test_payload["repos_url"])
            
            # Verify org property was called
            mock_org.assert_called_once()

    @patch('client.GithubOrgClient.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test the public_repos method
        """
        # Test payload for repos
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        
        # Mocked repos URL
        test_repos_url = "https://api.github.com/orgs/test-org/repos"
        
        # Use multiple patches to mock get_json and _public_repos_url
        with patch('client.GithubOrgClient._public_repos_url', 
                   new_callable=PropertyMock, 
                   return_value=test_repos_url) as mock_repos_url:
            # Configure get_json to return test payload
            mock_get_json.return_value = test_payload
            
            # Create client instance
            gh_client = GithubOrgClient("test-org")
            
            # Get public repos
            result = gh_client.public_repos()
            
            # Check result is list of repo names
            self.assertEqual(result, ["repo1", "repo2"])
            
            # Verify mocks were called once
            mock_get_json.assert_called_once_with(test_repos_url)
            mock_repos_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test the has_license method with parametrized inputs
        """
        # Create client instance
        gh_client = GithubOrgClient("test-org")
        
        # Check if repo has the specified license
        result = gh_client.has_license(repo, license_key)
        
        # Assert result matches expected value
        self.assertEqual(result, expected)


@parameterized_class(('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), [
    (org_payload, repos_payload, expected_repos, apache2_repos)
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""
    
    @classmethod
    def setUpClass(cls):
        """
        Set up class method to mock requests
        """
        # Start a patcher for requests.get
        cls.get_patcher = patch('requests.get')
        
        # Create the mock
        cls.mock_get = cls.get_patcher.start()
        
        # Configure side_effect to return correct fixtures
        def side_effect(url):
            class MockResponse:
                def __init__(self, json_data):
                    self.json_data = json_data
                
                def json(self):
                    return self.json_data
            
            if url == "https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == "https://api.github.com/orgs/google/repos":
                return MockResponse(cls.repos_payload)
            return None
        
        # Set the side effect
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class method to stop the patcher
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Integration test for public_repos method
        """
        # Create client instance
        gh_client = GithubOrgClient("google")
        
        # Get public repos
        result = gh_client.public_repos()
        
        # Assert result matches expected repos
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Integration test for public_repos method with license filter
        """
        # Create client instance
        gh_client = GithubOrgClient("google")
        
        # Get public repos with Apache 2.0 license
        result = gh_client.public_repos(license="apache-2.0")
        
        # Assert result matches apache2 repos
        self.assertEqual(result, self.apache2_repos)

if __name__ == '__main__':
    unittest.main()