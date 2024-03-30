import os
import unittest
from unittest.mock import patch
from fetch_article_html import extract_article_content

class TestArticleExtraction(unittest.TestCase):
    
    @patch('builtins.input', return_value="https://example.com/article")
    def test_pdf_generation(self, mock_input):
        extract_article_content("https://example.com/article")
        pdf_filename = os.path.join("articles", "sample_article_title.pdf")
        self.assertTrue(os.path.exists(pdf_filename))

    def test_html_content_creation(self):
        test_title = "Sample Article Title"
        test_publish_time = "2023-07-15"
        test_paragraphs = ["Paragraph 1", "Paragraph 2"]

        html_content = extract_article_content.create_html_content(test_title, test_publish_time, test_paragraphs)
        self.assertIn(test_title, html_content)
        self.assertIn(test_publish_time, html_content)
        for paragraph in test_paragraphs:
            self.assertIn(paragraph, html_content)
    
    def test_invalid_character_sanitization(self):
        invalid_title = 'Title with/invalid?characters*'
        sanitized_title = extract_article_content.sanitize_title(invalid_title)
        self.assertEqual(sanitized_title, 'Title with_invalid_characters_')

if __name__ == '__main__':
    unittest.main()
