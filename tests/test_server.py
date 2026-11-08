import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

import server


class ReviewTests(unittest.TestCase):
    def test_local_keywords_are_whole_words_and_three_suggestions(self):
        result = server.local_review('Stakeholder research using SQL', 'Research SQL roadmap')
        self.assertIn('research, sql', result['strengths'][0])
        self.assertIn('roadmap', result['missing_evidence'][0])
        self.assertEqual(len(server.validate_result(result)['improvements']), 3)
        self.assertIn('None found', server.local_review('researcher', 'research')['strengths'][0])

    @patch.dict('os.environ', {'OPENROUTER_API_KEY': 'sk-or-v1-replace-with-your-key'})
    def test_placeholder_never_calls_provider(self):
        with patch('urllib.request.urlopen') as request:
            with self.assertRaisesRegex(RuntimeError, 'Add a valid'):
                server.ai_review('resume', 'job')
            request.assert_not_called()

    @patch.dict('os.environ', {'OPENROUTER_API_KEY': 'test-only-not-a-real-key'})
    def test_provider_request_and_validated_response(self):
        result = {'strengths': ['Evidence'], 'missing_evidence': ['Gap'], 'improvements': ['One', 'Two', 'Three']}
        response = io.BytesIO(json.dumps({'choices': [{'message': {'content': json.dumps(result)}}]}).encode())
        with patch('urllib.request.urlopen', return_value=response) as request:
            actual, _ = server.ai_review('resume evidence', 'job requirements')
            self.assertEqual(actual, result)
            body = json.loads(request.call_args[0][0].data)
            self.assertEqual(json.loads(body['messages'][1]['content'])['resume'], 'resume evidence')
            self.assertNotIn('test-only', json.dumps(body))

    @patch.dict('os.environ', {'OPENROUTER_API_KEY': 'test-only-not-a-real-key'})
    def test_provider_errors_are_sanitized(self):
        error = HTTPError('https://openrouter.ai', 401, 'private provider detail', {}, None)
        with patch('urllib.request.urlopen', side_effect=error):
            with self.assertRaisesRegex(RuntimeError, '^OpenRouter rejected the API key.$'):
                server.ai_review('resume', 'job')

    def test_rejects_bad_model_output(self):
        for result in ({}, {'strengths': ['x'], 'missing_evidence': ['x'], 'improvements': ['one']}, {'strengths': [5], 'missing_evidence': ['x'], 'improvements': ['a', 'b', 'c']}):
            with self.assertRaises(ValueError):
                server.validate_result(result)


if __name__ == '__main__':
    unittest.main()
