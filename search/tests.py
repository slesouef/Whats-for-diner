"""
Test file for the search algorithm
"""
from django.test import TestCase

from .search import get_results


class SearchTest(TestCase):
    """
    Verify that the search algorithm returns the expected sets from fixture
    """
    fixtures = ["test_recipes.json"]

    def test_search_single_term(self):
        """Validate the search behaviour when searching with a single term"""
        results = get_results("chorizo")
        self.assertEqual(4, len(results))
        self.assertEqual(1, results[0].id)
        self.assertEqual(2, results[1].id)
        self.assertEqual(4, results[2].id)
        self.assertEqual(7, results[3].id)

    def test_search_multiple_terms(self):
        """Validate the search behaviour when searching with multiple terms"""
        results = get_results("galette, champignons")
        self.assertEqual(7, len(results))
        self.assertEqual(1, results[0].id)
        self.assertEqual(2, results[1].id)
        self.assertEqual(3, results[2].id)
        self.assertEqual(5, results[3].id)
        self.assertEqual(6, results[4].id)
        self.assertEqual(8, results[5].id)
        self.assertEqual(9, results[6].id)

    def test_landing_view(self):
        """Test the landing page is displayed properly"""
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/landing.html")

    def test_landing_view_post(self):
        """Test the landing page is displayed properly"""
        context_data = {"query": "champignons"}
        response = self.client.post("/", data=context_data)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/results.html")
