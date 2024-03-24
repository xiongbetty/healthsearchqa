#!/usr/bin/env python3

import unittest

# import review_worksheets
from utils import get_reviewer_csv_files
from reviewer_report import load_data, calculate_mean
from review_worksheets import get_model_scores

class Tests(unittest.TestCase):
    @classmethod
    def setUp(self):
        self.folder_path = "tests"
        self.benchmark = "complete"
        self.scores_scheme = "1,2,3,4,5"

        self.csv_files = get_reviewer_csv_files(self.folder_path)
        self.reviewers = [d["reviewer"] for d in self.csv_files if "reviewer" in d]
        self.review_jsons = load_data(self.csv_files)

    def test_get_reviewer_csv_files(self):
        """
        This tests the function to get reviewer csv files
        """
        self.assertEqual(self.reviewers,['reviewer_1.csv', 'reviewer_2.csv'])
        self.assertEqual(self.csv_files, 
                         [{'reviewer': 'reviewer_1.csv', 'file_path': 'tests/reviewer_1.csv'}, 
                          {'reviewer': 'reviewer_2.csv', 'file_path': 'tests/reviewer_2.csv'}])
        
    def test_calculate_mean(self):
        """
        This tests the function to calculate mean
        """
        mean_scores = calculate_mean(self.reviewers, self.review_jsons, self.benchmark)
        self.assertEqual(mean_scores,
                         {'reviewer_1.csv': {5: 0, 4: 0, 3: 0, 2: 0, 1: 3}, 
                          'reviewer_2.csv': {5: 1, 4: 2, 3: 0, 2: 0, 1: 0}})

    def test_get_model_scores(self):
        """
        This tests the function to get the average of all model scores
        """
        model_scores = get_model_scores(self.review_jsons)
        self.assertEqual(model_scores,
                         {'biogpt': {'complete': 4.0, 'error_free': 4.0, 'appropriate': 4.0, 'harm_extent': 4.0, 'harm_likelihood': 5.0, 'no_bias': 5.0, 'total': 1}, 
                          'biomedlm': {'complete': 2.4, 'error_free': 4.4, 'appropriate': 3.2, 'harm_extent': 4.0, 'harm_likelihood': 4.4, 'no_bias': 4.8, 'total': 5}, 
                          'llama': {'complete': 0, 'error_free': 0, 'appropriate': 0, 'harm_extent': 0, 'harm_likelihood': 0, 'no_bias': 0, 'total': 0}, 
                          'mistral': {'complete': 0, 'error_free': 0, 'appropriate': 0, 'harm_extent': 0, 'harm_likelihood': 0, 'no_bias': 0, 'total': 0}})

if __name__ == "__main__":
    unittest.main()