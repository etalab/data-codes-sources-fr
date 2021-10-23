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

        # with self.assertRaises(NotImplementedError):
        #     self.detector.find_platform("http://sourcesup.renater.fr")

    def test_platform_base_url(self):
        self.assertEquals(
            self.detector.platform_base_url("https://github.com/etalab"),
            "https://api.github.com/",
        )
        self.assertEquals(
            self.detector.platform_base_url("https://gitlab.com/pidila"),
            "https://gitlab.com/api/v4/",
        )

    def test_to_orgs(self):
        org = self.detector.to_orgs("https://github.com/etalab/")

        self.assertEquals(len(org), 1)
        self.assertIsInstance(org[0], GitHubOrg)
        self.assertEquals(org[0].organization, "etalab")
        self.assertEquals(org[0].base_url, "https://api.github.com/")

        org = self.detector.to_orgs("https://framagit.org/etalab")
        self.assertEquals(len(org), 1)
        self.assertIsInstance(org[0], GitLabOrg)
        self.assertEquals(org[0].organization, "etalab")
        self.assertEquals(org[0].base_url, "https://framagit.org/api/v4/")

    def test_is_bare_platform(self):
        self.assertTrue(self.detector.is_bare_platform("https://gitlab.adullact.net/"))
        self.assertTrue(self.detector.is_bare_platform("https://gitlab.adullact.net"))
        self.assertFalse(
            self.detector.is_bare_platform("https://gitlab.adullact.net/aife")
        )
        self.assertFalse(self.detector.is_bare_platform("https://github.com"))

    def test_find_orgs(self):
        res = self.detector.find_orgs("https://gitlab.adullact.net")

        self.assertIsInstance(res, list)
        for item in res:
            self.assertIsInstance(item, GitLabOrg)
