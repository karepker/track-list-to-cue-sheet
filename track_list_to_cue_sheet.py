"""
Generates a cue file based on a track list.
"""

__author__ = 'Kar Epker'
__copyright__ = '2016, karepker@gmail.com (Kar Epker)'


import argparse
import csv
import datetime
import logging
import os
import sys


def parse_track_string(track, name_index, time_index):
    """Parses a track string and returns the name and time.

    Args:
        track: A csv row read in.
        name_index: The index in the csv row that contains the track name.
        time_index: The index in the csv row that contains the track's elapsed
                    time.
    Raises: A ValueError if there are not enough entries in the row.
    Returns: The name of the track and its duration as a timedelta.
    """
    if len(track) < max(name_index, time_index) + 1:
        raise ValueError(
                'Not enough fields for track {}, skipping.'.format(track))

    name = track[name_index]
    time_string = track[time_index]

    logger = logging.getLogger(__name__)
    logger.debug('Got name %s and time %s.', name, time_string)

    # Read the time portion of the string
    total_seconds = 0
    split_time_string = time_string.split(':')
    if len(split_time_string) > 3:
        raise ValueError(
                'Skipping track {} with unparseable time.'.format(track))

    time_parts = ['0'] * (3 - len(split_time_string)) + split_time_string
    hours, minutes, seconds = time_parts
    try:
        total_seconds = (int(hours) * 60 * 60 + int(minutes) * 60 +
                          int(seconds))
    # Invalid time value
    except ValueError:
        raise ValueError(
            'Skipping track {} with unparseable time {}.'.format(track,
                                                                 time_string))

    logger.debug('Parsed %d seconds for track "%s".', total_seconds, track)

    return name, datetime.timedelta(seconds=total_seconds)


def create_cue_sheet(names, performers, track_times,
                     start_time=datetime.timedelta(seconds=0)):
    """Yields the next cue sheet entry given the track names, times.

    Args:
        names: List of track names.
        track_times: List of timdeltas containing the track times.
        performers: List of performers to associate with each cue entry.
        start_time: The initial time to start the first track at.

    The lengths of names and track times should be the same.
    """
    accumulated_time = start_time

    for track_index, (name, performer, track_time) in enumerate(
            zip(names, performers, track_times)):
        minutes = int(accumulated_time.total_seconds() / 60)
        seconds = int(accumulated_time.total_seconds() % 60)

        cue_sheet_entry = '''  TRACK {:02} AUDIO
    TITLE {}
    PERFORMER {}
    INDEX 01 {:02d}:{:02d}:00'''.format(track_index, name, performer, minutes,
                                        seconds)
        accumulated_time += track_time
        yield cue_sheet_entry


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates a cue sheet given '
                                     'a track list.')
    parser.add_argument('track_list', nargs='?', type=argparse.FileType('r'),
            default=sys.stdin, help='File to segment (default standard input).')
    parser.add_argument('--name-index', dest='name_index', default=1, type=int,
                        help='The index of the column in the track list '
                        'containing the track name.')
    parser.add_argument('--time-index', dest='time_index', default=3, type=int,
                        help='The index of the column in the track list '
                        'containing the track\'s elapsed time.')
    parser.add_argument('--performer', dest='performer', required=True,
            help='The performer to be attributed by PERFORMER.')
    parser.add_argument('--start-seconds', dest='start_seconds', type=int,
                        default=0, help='Start time of the first track in '
                        'seconds.')
    parser.add_argument('--title', dest='title', help='Title of the disc.')
    parser.add_argument('--rem', dest='rem', nargs='*', help='Rem attributes. '
                        'Specify as, e.g. "GENRE Pop"')
    parser.add_argument('--audio-file', dest='audio_file', required=True,
                        type=argparse.FileType('r'),
                        help='The audio file corresponding to cue sheet this '
                        'script will generate. This file will be used to infer '
                        'its name for the cue sheet FILE attribute.')
    parser.add_argument('--output-file', dest='output_file', default=sys.stdout,
                        type=argparse.FileType('w'),
                        help='The location to print the output cue file. '
                        'By default, stdout.')
    parser.add_argument('--debug', dest='log_level', default=logging.WARNING,
                        action='store_const', const=logging.DEBUG,
                        help='Print debug log statements.')
    parser.add_argument('--dummy', dest='dummy', action='store_true',
                        help='Add dummy track at the end (true by default).')
    parser.add_argument('--no-dummy', dest='dummy', action='store_false',
                        help='Do not add dummy track at the end.')

    parser.set_defaults(dummy=True)
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stderr, level=args.log_level)
    logger = logging.getLogger(__name__)

    start = datetime.timedelta(seconds=args.start_seconds)

    track_times = []
    names = []
    # TODO: Add ability to get performers by parsing track file.
    performers = []
    for track in csv.reader(args.track_list, delimiter='\t'):
        try:
            name, track_time = parse_track_string(track, args.name_index,
                                                  args.time_index)
            names.append(name)
            performers.append(args.performer)
            track_times.append(track_time)
        except ValueError as v:
            logger.error(v)

    # The dummy track is required to make mp3splt split the last track.
    if args.dummy:
        names.append("Dummy track")
        performers.append(args.performer)
        track_times.append(datetime.timedelta(seconds=0))

    output_file = args.output_file

    output_file.writelines('REM {}\n'.format(rem) for rem in args.rem)
    output_file.writelines('PERFORMER {}\n'.format(args.performer))

    if args.title:
        output_file.writelines('TITLE {}\n'.format(args.title))

    audio_file_name = os.path.basename(args.audio_file.name)
    audio_file_extension = os.path.splitext(args.audio_file.name)[1][1:].upper()
    output_file.writelines('FILE "{}" {}\n'.format(audio_file_name,
                                                 audio_file_extension))

    output_file.writelines(
        '{}\n'.format(cue_entry) for cue_entry in create_cue_sheet(
                names, performers, track_times, start))
