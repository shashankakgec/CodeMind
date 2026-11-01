import unittest
from unittest.mock import MagicMock, patch

from backend.services import bug_classifier


class BugClassifierStatusTests(unittest.TestCase):
    def test_status_does_not_publish_unverified_metrics(self):
        with patch.object(bug_classifier, "HF_TOKEN", None):
            status = bug_classifier.get_status()

        self.assertIsNone(status["accuracy"])
        self.assertIsNone(status["f1_macro"])
        self.assertFalse(status["metrics_available"])
        self.assertFalse(status["configured"])

    def test_unknown_model_label_is_not_silently_mapped_to_class_zero(self):
        with patch.object(bug_classifier, "HF_TOKEN", "test-token"):
            response = MagicMock()
            response.status_code = 200
            response.json.return_value = [[{"label": "LABEL_1", "score": 0.91}]]

            client = MagicMock()
            client.__enter__.return_value.post.return_value = response

            with patch.object(bug_classifier.httpx, "Client", return_value=client):
                result = bug_classifier.predict("def example(): return 1")

        self.assertEqual(result["predicted_class"], "unmapped_label")
        self.assertIsNone(result["predicted_label"])
        self.assertFalse(result["is_bug"])

    def test_known_label_uses_declared_mapping(self):
        with patch.object(bug_classifier, "HF_TOKEN", "test-token"):
            response = MagicMock()
            response.status_code = 200
            response.json.return_value = [[{"label": "sql_injection", "score": 0.91}]]

            client = MagicMock()
            client.__enter__.return_value.post.return_value = response

            with patch.object(bug_classifier.httpx, "Client", return_value=client):
                result = bug_classifier.predict("query = input()")

        self.assertEqual(result["predicted_class"], "sql_injection")
        self.assertEqual(result["predicted_label"], bug_classifier.LABEL_NAMES.index("sql_injection"))
        self.assertTrue(result["is_bug"])


if __name__ == "__main__":
    unittest.main()
