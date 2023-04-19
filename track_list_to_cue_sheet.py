"""
Generates a cue file based on a track list.
"""

__author__ = 'Kar Epker'
__copyright__ = '2016–2023, karepker@gmail.com (Kar Epker)'

import argparse
import csv
import datetime
import logging
import os
import sys


def parse_time_string(time_string):
    """Parses time string consisting of [hh:mm:]ss into a timedelta object.

    Raises: A ValueError if the time string could not be parsed.
    """
    total_seconds = 0
    split_time_string = time_string.split(':')
    if len(split_time_string) > 3:
        raise ValueError('Time {} has too many parts {} > 3.'.format(
            time_string, len(split_time_string)))

    # Pad split_time_string with explicit values of 0 for hours and minutes if
    # they are not provided.
    time_parts = ['0'] * (3 - len(split_time_string)) + split_time_string
    hours, minutes, seconds = time_parts
    total_seconds = (int(hours) * 60 * 60 + int(minutes) * 60 + int(seconds))

    logger = logging.getLogger(__name__)
    logger.debug('Parsed %d seconds for time string "%s".', total_seconds,
                 time_string)

    return datetime.timedelta(seconds=total_seconds)


def parse_track_string(track):
    """Parses a track string and returns the name and time.

    Args:
        track: A csv row read in.
    Raises: A ValueError if there are not enough entries in the row.
    Returns: The name of the track, its duration as a timedelta, and the
        performer for the track.
    """
    sanitized_performer_index = (args.performer_index
                                 if args.performer_index else 0)
    if len(track) < (max(args.name_index, args.time_index, args.performer_index
                         if args.performer_index else 0) + 1):
        raise ValueError(
            'Not enough fields for track {}, skipping.'.format(track))

    name = track[args.name_index]
    time_string = track[args.time_index]
    performer = (track[args.performer_index]
                 if args.performer_index else args.performer)

    logger = logging.getLogger(__name__)
    logger.debug('Got name %s, time %s, and performer %s.', name, time_string,
                 performer)

    return name, parse_time_string(time_string), performer


def parse_tracks(tracks):
    """Parses track metadata from given track iterable.

    Args:
        tracks: Iterable of tracks to loop over.

    Raises: A ValueError if a track could not be parsed.
    Yields: A 3-tuple of track metadata:
        * Timedelta representing the start of the track.
        * Name.
        * List of performers for the track.
    """
    accumulated_time = args.start_time
    for track in csv.reader(args.track_list, delimiter='\t'):
        try:
            name, track_time, performer = parse_track_string(track)

            if args.timestamp:
                yield (track_time, name, performer)
            else:
                yield (accumulated_time, name, performer)
                accumulated_time += track_time
        except ValueError as v:
            logger.error(v)

    # The dummy track is required to make mp3splt split the last track.
    if args.dummy:
        if args.timestamp:
            yield (args.end_time, "Dummy track", args.performer)
        else:
            yield (accumulated_time, "Dummy track", args.performer)


def create_cue_sheet(tracks):
    """Yields the next cue sheet entry given the track names, times.

    Args:
        tracks: An iterable of 3-tuples containing metadata about each track:
            * Name.
            * Timedelta representing the start of the track.
            * List of performers for the track.
    """
    for track_index, (track_time, name, performer) in enumerate(tracks):
        minutes = int(track_time.total_seconds() / 60)
        seconds = int(track_time.total_seconds() % 60)

        cue_sheet_entry = '''  TRACK {:02} AUDIO
    TITLE {}
    PERFORMER {}
    INDEX 01 {:02d}:{:02d}:00'''.format(track_index, name, performer, minutes,
                                        seconds)
        yield cue_sheet_entry


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates a cue sheet given '
                                     'a track list.')
    parser.add_argument('track_list',
                        nargs='?',
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help='File to segment (default standard input).')
    parser.add_argument('--name-index',
                        dest='name_index',
                        type=int,
                        required=True,
                        help='The index of the column in the track list '
                        'containing the track name.')
    parser.add_argument('--time-index',
                        dest='time_index',
                        required=True,
                        type=int,
                        help='The index of the column in the track list '
                        'containing the track\'s elapsed time.')
    parser.add_argument('--performer-index',
                        dest='performer_index',
                        type=int,
                        help='The index of the column in the track list '
                        'containing the track\'s performers. If not given, '
                        'defaults to the performer ')
    parser.add_argument('--performer',
                        dest='performer',
                        required=True,
                        help='The performer to be attributed at the album '
                        'level. Will also be used for individual tracks '
                        'unless a performer index is given.')
    parser.add_argument('--start-time',
                        dest='start_time',
                        type=parse_time_string,
                        default=datetime.timedelta(seconds=0),
                        help='Start time of the first track in seconds. '
                        'Only used when timestamp is false.')
    parser.add_argument('--end-time',
                        dest='end_time',
                        type=parse_time_string,
                        default=datetime.timedelta(seconds=0),
                        help='End time of the last track in seconds. '
                        'Only used when timestamp and dummy are true.')
    parser.add_argument('--title', dest='title', help='Title of the disc.')
    parser.add_argument('--rem',
                        dest='rem',
                        nargs='*',
                        help='Rem attributes. '
                        'Specify as, e.g. "GENRE Pop"')
    parser.add_argument(
        '--audio-file',
        dest='audio_file',
        required=True,
        type=argparse.FileType('r'),
        help='The audio file corresponding to cue sheet this '
        'script will generate. This file will be used to infer '
        'its name for the cue sheet FILE attribute.')
    parser.add_argument('--output-file',
                        dest='output_file',
                        default=sys.stdout,
                        type=argparse.FileType('w'),
                        help='The location to print the output cue file. '
                        'By default, stdout.')
    parser.add_argument('--debug',
                        dest='log_level',
                        default=logging.WARNING,
                        action='store_const',
                        const=logging.DEBUG,
                        help='Print debug log statements.')
    parser.add_argument(
        '--timestamp',
        dest='timestamp',
        action='store_true',
        default=False,
        help='Whether the times associated with each track are '
        'timestamps, i.e. they describe the time in the file '
        'when the track starts.')
    parser.add_argument('--dummy',
                        dest='dummy',
                        action='store_true',
                        help='Add dummy track at the end (true by default).')
    parser.add_argument('--no-dummy',
                        dest='dummy',
                        action='store_false',
                        help='Do not add dummy track at the end.')

    parser.set_defaults(dummy=True)
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stderr, level=args.log_level)
    logger = logging.getLogger(__name__)

    tracks = parse_tracks(csv.reader(args.track_list, delimiter='\t'))

    output_file = args.output_file

    output_file.writelines('REM {}\n'.format(rem) for rem in args.rem)
    output_file.writelines('PERFORMER {}\n'.format(args.performer))

    if args.title:
        output_file.writelines('TITLE {}\n'.format(args.title))

    audio_file_name = os.path.basename(args.audio_file.name)
    audio_file_extension = os.path.splitext(
        args.audio_file.name)[1][1:].upper()
    output_file.writelines('FILE "{}" {}\n'.format(audio_file_name,
                                                   audio_file_extension))

    output_file.writelines('{}\n'.format(cue_entry)
                           for cue_entry in create_cue_sheet(tracks))
