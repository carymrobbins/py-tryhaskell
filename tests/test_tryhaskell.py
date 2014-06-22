import unittest
from tryhaskell import TryHaskell


class UnitTest(unittest.TestCase):
    success_json = {
        'success': {
            'expr': 'putStrLn ("foo" ++ "bar") >> return "baz',
            'files': [],
            'stdout': ['foobar'],
            'type': 'IO [Char]',
            'value': '"baz"',
        }
    }

    error_json = {'error': "Not in scope, `foobar'\n"}

    def test_bad_result_not_ok(self):
        self.assertFalse(TryHaskell._bad_result('error message').ok)

    def test_parse(self):
        self.assertTrue(TryHaskell.parse(self.success_json).ok)
        self.assertFalse(TryHaskell.parse(self.error_json).ok)

    def test_show(self):
        show = lambda j: TryHaskell.show(TryHaskell.parse(j))
        out = '{0}\n{1}'.format(
            '\n'.join(self.success_json['success']['stdout']),
            self.success_json['success']['value'])
        self.assertEqual(out, show(self.success_json))
        out = self.error_json['error'].strip()
        self.assertEqual(out, show(self.error_json))


class IntegrationTest(unittest.TestCase):
    def test_eval(self):
        expressions = [
            ('map (*2) [1,2,3]', '[2,4,6]'),
            ('''show "foo"''', r'"\"foo\""'),
            ('[x `div` y | x <- [6,8,10], y <- [4,5,6]]', '[1,1,1,2,1,1,2,2,1]')
        ]
        for exp, result in expressions:
            self.assertEqual(TryHaskell.eval(exp), result)

    def test_error(self):
        result = TryHaskell.get('foobar')
        self.assertFalse(result.ok)


if __name__ == '__main__':
    unittest.main()
