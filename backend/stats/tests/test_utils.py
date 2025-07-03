from django.test import TestCase
from stats.utils import format_battletag, format_stat_value, calculate_difference

class UtilsTestCase(TestCase):
    def test_format_battletag(self):
        self.assertEqual(format_battletag('Player#1234'), 'Player-1234')

    def test_format_stat_value(self):
        self.assertEqual(format_stat_value('time_played', 3661), '1h 1m')
        self.assertEqual(format_stat_value('eliminations', 42), '42')
        self.assertEqual(format_stat_value('eliminations', None), 'N/A')

    def test_calculate_difference(self):
        self.assertEqual(calculate_difference('eliminations', 10, 5), '+5')
        self.assertEqual(calculate_difference('eliminations', 5, 10), '-5')
        self.assertEqual(calculate_difference('time_played', 3661, 61), '+1h 0m')
        self.assertEqual(calculate_difference('eliminations', 'a', 5), 'N/A')
