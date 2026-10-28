"""Check a built homepage: python tests/test_homepage.py /path/to/jekyll-output.

Requires lxml, available in the bundled Codex Python runtime.
"""

from pathlib import Path
import sys
import unittest
from urllib.parse import urlsplit

from lxml import html


BUILD = Path(sys.argv.pop(1)) if len(sys.argv) > 1 else Path("_site")


class HomepageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = html.parse(str(BUILD / "index.html"))
        cls.body = cls.page.find("body")
        cls.papers = cls.page.xpath('//article[contains(@class, "publication-item")]')

    def test_homepage_specific_layout(self):
        self.assertEqual(self.body.get("class"), "homepage")
        self.assertTrue(self.page.xpath('//link[contains(@href, "/assets/css/homepage.css")]'))
        self.assertTrue((BUILD / "assets/css/homepage.css").is_file())

    def test_opportunities_precede_introduction(self):
        text = " ".join(self.body.text_content().split())
        notice = "Seeking 2027 full-time and internship opportunities"
        self.assertIn(notice, text)
        self.assertLess(text.index(notice), text.index("I am a fourth-year"))
        self.assertNotIn("UCLA \u00b7 AI research", text)
        self.assertFalse(self.page.xpath('//div[@class="preview-bar"]'))

    def test_profile_preserves_contact_preferences(self):
        profiles = self.page.xpath('//aside[@aria-label="Profile and contact information"]')
        self.assertEqual(len(profiles), 1)
        profile = profiles[0]
        self.assertIn("Los Angeles and Bay Area", profile.text_content())
        links = profile.xpath('.//a/@href')
        self.assertEqual(len(links), 3)
        self.assertIn("mailto:peiran@ucla.edu", links)
        self.assertTrue(any("linkedin.com/in/peiranx" in link for link in links))
        self.assertTrue(any("scholar.google.com" in link and "K5zRJC8AAAAJ" in link for link in links))
        self.assertFalse(any("github" in link or "instagram" in link or "cv.pdf" in link for link in links))

    def test_requested_introduction(self):
        introduction = self.page.xpath('//div[@class="home-intro-text"]')[0]
        paragraphs = [" ".join(p.text_content().split()) for p in introduction.xpath('./p')]
        self.assertEqual(paragraphs, [
            "I am a fourth-year Ph.D. candidate at UCLA, where I am fortunate to be advised by Prof. Debiao Li. My research interests include LLM post-training, LLM agents, Agentic RL and AI for Healthcare.",
            "I have also enjoyed my time as a research intern at Snowflake AI Research, Alibaba, and JHU. Before joining UCLA, I received my bachelor\u2019s degree from Shanghai Jiao Tong University.",
        ])
        self.assertEqual(introduction.xpath('.//strong/text()'), ["LLM post-training, LLM agents, Agentic RL and AI for Healthcare"])
        self.assertIn("AI for Healthcare", self.page.xpath('//meta[@property="og:description"]/@content')[0])

    def test_experience_name_and_dates(self):
        jobs = self.page.xpath('//*[@id="experience"]//article')
        self.assertEqual(len(jobs), 2)
        self.assertEqual(jobs[0].xpath('.//h3/text()'), ["Snowflake AI Research"])
        self.assertIn("Sep 2026", jobs[0].text_content())
        self.assertNotIn("present", jobs[0].text_content())
        self.assertFalse(self.page.xpath('//*[@id="experience"]//a'))
        self.assertFalse(self.page.xpath('//*[@id="about"]//a'))

    def test_seven_selected_publications_in_requested_order(self):
        titles = [p.xpath('.//h3')[0].text_content() for p in self.papers]
        self.assertEqual(len(titles), 7)
        starts = ["HybridResearcher:", "Benchmarking Hybrid Deep Research", "Hybrid Reward Normalization", "Agents' Last Exam", "AtlasGS:", "Hawkeye:", "FedConv:"]
        for title, prefix in zip(titles, starts):
            self.assertTrue(title.startswith(prefix), title)
        self.assertNotIn("One-Shot Physics-Guided", self.body.text_content())
        self.assertNotIn("ISMRM", self.body.text_content())
        self.assertNotIn("Weakly-Supervised Learning", self.body.text_content())
        self.assertNotIn("Brain Age Gap Prediction", self.body.text_content())
        for paper in self.papers:
            self.assertIn("Peiran Xu", paper.xpath('.//strong/text()'))

    def test_new_resources_and_summaries(self):
        self.assertEqual(len(self.page.xpath('//a[normalize-space(text())="Blog"]')), 2)
        self.assertNotIn("Technical write-up", self.body.text_content())
        self.assertEqual(len(self.papers[0].xpath('.//a[contains(@href, "hybridresearcher-deep-research-agents")]')), 1)
        self.assertEqual(len(self.papers[1].xpath('.//a[contains(@href, "hybrid-deep-research-benchmark")]')), 1)
        self.assertEqual(len(self.papers[1].xpath('.//a[contains(@href, "hybrid_leaderboard")]')), 1)
        self.assertEqual(len(self.page.xpath('//p[@class="publication-summary"]')), 4)
        self.assertIn("NeurIPS 2026", self.papers[3].text_content())
        for paper in self.papers:
            self.assertTrue(paper.xpath('.//p[@class="publication-meta"]'))
            self.assertTrue(paper.xpath('.//a[normalize-space(text())="Paper"]'))

    def test_local_images_and_dimensions(self):
        figures = self.page.xpath('//img[@class="publication-image"]')
        self.assertEqual(len(figures), 7)
        for image in self.page.xpath('//img'):
            self.assertTrue(image.get("alt"))
            self.assertGreater(int(image.get("width", 0)), 0)
            self.assertGreater(int(image.get("height", 0)), 0)
            path = urlsplit(image.get("src")).path.lstrip("/")
            self.assertTrue((BUILD / path).is_file(), path)

    def test_navigation_and_semantics(self):
        self.assertEqual(self.page.xpath('//a[@class="home-brand"]/text()'), ["Homepage"])
        self.assertEqual(self.page.xpath('//h2[@id="publications-heading"]/text()'), ["Selected Publications"])
        self.assertEqual(self.page.xpath('//nav//a[@href="#publications"]/text()'), ["Selected Publications"])
        self.assertEqual(len(self.page.xpath('//h1')), 1)
        self.assertEqual(len(self.page.xpath('//main')), 1)
        for anchor in self.page.xpath('//a[starts-with(@href, "#")]'):
            self.assertTrue(self.page.xpath('//*[@id=$id]', id=anchor.get("href")[1:]))
        self.assertTrue(self.page.xpath('//a[@class="home-skip-link"]'))

    def test_development_files_not_published(self):
        self.assertFalse((BUILD / "tests/test_homepage.py").exists())
        self.assertFalse((BUILD / "docs/superpowers/plans/2026-10-27-homepage-refresh.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
