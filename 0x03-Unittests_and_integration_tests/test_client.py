#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from unittest.mock import PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        mock_get_json.return_value = {"name": org_name, "type": "Organization"}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, {"name": org_name, "type": "Organization"})

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url property."""
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
        client = GithubOrgClient("google")
        result = client._public_repos_url
        self.assertEqual(result, "https://api.github.com/orgs/google/repos")

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_repos_url, mock_get_json):
        """Test public_repos method."""
        mock_repos_url.return_value = "https://api.github.com/orgs/google/repos"
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        client = GithubOrgClient("google")
        result = client.public_repos
        self.assertEqual(result, ["repo1", "repo2"])
        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/google/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method."""
        client = GithubOrgClient("google")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {"org_payload": org_payload, "repos_payload": repos_payload,
     "expected_repos": expected_repos, "apache2_repos": apache2_repos},
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test suite for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Set up class with mocked requests."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()
        mock_get.side_effect = cls.mocked_requests

    @classmethod
    def tearDownClass(cls):
        """Tear down class by stopping the patch."""
        cls.get_patcher.stop()

    @staticmethod
    def mocked_requests(url):
        """Mock requests.get based on URL."""
        if "orgs/google" in url:
            return MockResponse(org_payload)
        elif "repos" in url:
            return MockResponse(repos_payload)
        return None

    def test_public_repos(self):
        """Test public_repos method with fixtures."""
        client = GithubOrgClient("google")
        result = client.public_repos
        self.assertEqual(result, expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos method with a license argument."""
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, apache2_repos)


class MockResponse:
    """Mock response object for requests.get."""

    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        """Return the mocked JSON data."""
        return self.json_data


if __name__ == "__main__":
    unittest.main()
