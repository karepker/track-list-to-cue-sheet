# Track list to cue sheet

This is a script that converts a list of tracks with associated times to a [cue
sheet], which is used to describe the tracks in a single audio/video file or
disc.

This script supports track lists in two formats:

* Track runtime-style, where each time associated with a track in the input file
  describes the runtime of that individual track.
* Timestamp-style, where each time associated with a track in the input file
  gives the timestamp when the track begins.

Personally, I use it to generate a cue sheets to allow splitting of a single
audio track into their component tracks using, e.g. [mp3splt].

This script only supports tab separated value (tsv) track lists.

## Usage

See the test script for example commands in both track runtime style and
timestamp style.

`python track_list_to_cue_sheet.py` will list all options.

## Testing

Run `test.sh`, which will exit with the number of failed tests.

## License

MIT License; see included file.

[cue sheet]: https://en.wikipedia.org/wiki/Cue_sheet_(computing)
[mp3splt]: https://en.wikipedia.org/wiki/Mp3splt
