#! /bin/bash

# A simple test harness for track_list_to_cue_sheet that verifies a known input
# against a given output.

python track_list_to_cue_sheet.py testdata/rockapella_in_concert.tsv \
  --performer Rockapella --title "In Concert" --start-seconds 50 \
  --rem "GENRE Pop" "DATE 2001" --name-index 1 --time-index 3 \
  --audio-file="testdata/rockapella_in_concert.mp3" \
  | diff - testdata/rockapella_in_concert.cue

if (( $? == 0 )); then
	echo "Success!";
else
	echo "Failed";
fi
