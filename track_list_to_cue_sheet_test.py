"""
Tests for the track_list_to_cue_sheet.
"""

__author__ = "Kar Epker (karepker@gmail.com)"
__copyright__ = "Kar Epker, 2015"


import os
import unittest

from datetime import timedelta
from track_list_to_cue_sheet import *


class TrackListToCueSheetTest(unittest.TestCase):
    """Tests the SimpleDatedEntry class."""

    def test_parse_track_string(self):
        """Tests the parse_track_string function."""

        # Normal condition.
        self.assertEqual(
            parse_track_string(['1.', 'Name', 'Irrelevant', '1:00']),
            ('Name', timedelta(seconds=60)))

        # Not enough fields.
        with self.assertRaises(ValueError):
            parse_track_string('1.\tName\tIrrelevant\t')

    def test_create_cue_sheet(self):
        """Tests the cue sheet creation functionality."""

        # Normal test case.
        names = ["Example 1", "Example 2", "Example 3"]
        performers = ["Artist1", "Artist2", "Artist3"]
        track_times = [
            timedelta(seconds=30), timedelta(seconds=120),
            timedelta(seconds=45)]
        start_time = timedelta(seconds=30)

        cue_sheet_entries = [
            '''  TRACK 00 AUDIO
    TITLE Example 1
    PERFORMER Artist1
    INDEX 01 00:30:00''',
            '''  TRACK 01 AUDIO
    TITLE Example 2
    PERFORMER Artist2
    INDEX 01 01:00:00''',
            '''  TRACK 02 AUDIO
    TITLE Example 3
    PERFORMER Artist3
    INDEX 01 03:00:00''']

        self.assertEqual(list(create_cue_sheet(names, performers, track_times,
                                               start_time=start_time)),
                         cue_sheet_entries)


if __name__ == '__main__':
    unittest.main()
