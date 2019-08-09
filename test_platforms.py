import unittest

from platforms import Detector
from github import GitHubOrg
from gitlab import GitLabOrg


class TestPlatforms(unittest.TestCase):
    def setUp(self):
        self.detector = Detector()

    def test_find_domain(self):
        self.assertEquals(
            self.detector.find_domain("https://github.com/etalab"), "github.com"
        )

        with self.assertRaises(ValueError):
            self.detector.find_domain("http://example.fr")

    def test_find_platform(self):
        self.assertEquals(
            self.detector.find_platform("https://github.com/etalab"), "github"
        )

        with self.assertRaises(ValueError):
            self.detector.find_platform("http://example.fr")

        with self.assertRaises(NotImplementedError):
            self.detector.find_platform("http://sourcesup.renater.fr")

    def test_platform_base_url(self):
        self.assertEquals(
            self.detector.platform_base_url("https://github.com/etalab"),
            "https://api.github.com/",
        )
        self.assertEquals(
            self.detector.platform_base_url("https://gitlab.com/pidila"),
            "https://gitlab.com/api/v4/",
        )

    def test_to_org(self):
        org = self.detector.to_org("https://github.com/etalab/")

        self.assertIsInstance(org, GitHubOrg)
        self.assertEquals(org.organisation, "etalab")
        self.assertEquals(org.base_url, "https://api.github.com/")

        org = self.detector.to_org("https://gitlab.inria.fr/etalab")
        self.assertIsInstance(org, GitLabOrg)
        self.assertEquals(org.organisation, "etalab")
        self.assertEquals(org.base_url, "https://gitlab.inria.fr/api/v4/")
