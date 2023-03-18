#! /bin/bash

# A simple test harness for track_list_to_cue_sheet that verifies a known input
# against a given output.
# TODO: Clean up repeated validation code. Of course, this is bash, so it's
# a huge pain to do flow control if there are quotes and spaces involved.

num_tests_failed=0

python track_list_to_cue_sheet.py testdata/rockapella_in_concert.tsv \
  --performer Rockapella --title "In Concert" --start-time 50 \
  --rem "GENRE Pop" "DATE 2001" --name-index 1 --time-index 3 \
  --audio-file="testdata/rockapella_in_concert.mp3" \
  | diff - testdata/rockapella_in_concert.cue

if (( $? == 0 )); then
	echo "Rockapella test success!";
else
	echo "Rockapella test failed";
	((num_tests_failed++))
fi

python track_list_to_cue_sheet.py testdata/clap_it_up_dan.tsv \
  --performer "Clap It Up Dan" --title "Covers 2020–2021" \
  --timestamp --end-time 1:14:22 --rem "GENRE Christian" "DATE 2021" \
  --name-index 1 --time-index 0 --audio-file="testdata/clap_it_up_dan.mp3" \
  | diff - testdata/clap_it_up_dan.cue

if (( $? == 0 )); then
	echo "Clap It Up Dan test success!";
else
	echo "Clap It Up Dan test failed";
	((num_tests_failed++))
fi

exit $num_tests_failed
