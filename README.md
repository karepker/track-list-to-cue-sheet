# Track list to cue sheet

This is a simple script that converts list of tracks with elapsed time to a [cue
sheet], which is used to describe the tracks in a single audio/video file or
disc.

Personally, I use it to generate a cue sheets to allow splitting of a single
audio track into their component tracks using, e.g. [mp3splt].

This script only supports tab separated value (tsv) track lists with the track
name in column 1 (0-indexed) and elapsed time of the track in column 3. See
below for an example.

## Example usage

I wrote this script because I had a single long audio file I had ripped from
_Rockapella: Live in Concert_ DVD and wanted to convert it to single audio
files without having to manually find and split out each one.

I was planning on doing this with [mp3splt], which accepts a cue sheet as input,
but I could only find a Wikipedia entry containing the [track list of the
corresponding CD][rockapella_live_in_concert_cd]. I wrote this script to convert
that track list to a cue sheet.

Here is the command I used for the example.

```shell
python track_list_to_cue_sheet.py /tmp/rockapella_in_concert.txt \
--performer Rockapella --title "In Concert" --start-seconds 50 \
--rem "GENRE Pop" "DATE 2001" \
--audio-file="/home/karepker/Downloads/Rockapella Live in Concert.mp3" \
--output-file="/home/karepker/Downloads/Rockapella Live in Concert.cue"
```

The contents of `/tmp/rockapella_in_concert.txt` are included below.

``` text
1.	"I Am Your Man"	Scott Leonard	2:33
2.	"Dancin' In the Streets"	William Stevenson, Marvin Gaye	2:13
3.	"That's The Way"	Greg Clark, Scott Leonard	3:23
4.	"Let's Get Away From It All"	Tom Adair, Matt Dennis	2:15
5.	"This Isn't Love"	Scott Leonard, Greg Clark	4:36
6.	"Pretty Woman"	Roy Orbison, Bill Dees	3:04
7.	"Where in the World Is Carmen Sandiego?"	Sean Altman, David Yazbek	3:57
8.	"Blah Blah Blah"	Scott Leonard	2:51
9.	"Stand By Me"	Ben E. King, Mike Stoller, Jerry Leiber	3:14
10.	"Where Would We Be?"	Kevin Wright, Elliott Kerman	3:13
11.	"The Lion Sleeps Tonight"	Solomon Linda	2:38
12.	"Up on the Roof/Wonderful World"	Gerry Goffin, Carole King/Sam Cooke, Lou Adler, Herb Alpert	3:55
13.	"Tempted"	Chris Difford, Glenn Tilbrook	3:35
14.	"People Change"	Scott Leonard	3:41
15.	"Use Me"	Bill Withers	3:35
16.	"Dock of the Bay"	Otis Redding, Steve Cropper	3:24
17.	"Zombie Jamboree"	Conral Mauge, Jr.; Sean Altman (3rd verse lyrics)	3:40
18.	"Keep On Smilin'"	Jimmy Hall, Jack Hall, Lewis Ross, John Anthony, Ricky Hirsch	3:43
19.	"16 Tons"	Merle Travis	2:57
20.	"Moments Of You"	Scott Leonard	2:59
21.	"A Change In My Life"	Billy Straus	4:57
22.	"Long Cool Woman in a Black Dress"	Dummy	1:00
```

The output from this looked like:

```text
REM GENRE Pop
REM DATE 2001
PERFORMER Rockapella
TITLE In Concert
FILE "Rockapella Live in Concert.mp3" MP3
  TRACK 00 AUDIO
    TITLE I Am Your Man
    PERFORMER Rockapella
    INDEX 01 00:50:00
  TRACK 01 AUDIO
    TITLE Dancin' In the Streets
    PERFORMER Rockapella
    INDEX 01 03:23:00
  TRACK 02 AUDIO
    TITLE That's The Way
    PERFORMER Rockapella
    INDEX 01 05:36:00
  TRACK 03 AUDIO
    TITLE Let's Get Away From It All
    PERFORMER Rockapella
    INDEX 01 08:59:00
  TRACK 04 AUDIO
    TITLE This Isn't Love
    PERFORMER Rockapella
    INDEX 01 11:14:00
  TRACK 05 AUDIO
    TITLE Pretty Woman
    PERFORMER Rockapella
    INDEX 01 15:50:00
  TRACK 06 AUDIO
    TITLE Where in the World Is Carmen Sandiego?
    PERFORMER Rockapella
    INDEX 01 18:54:00
  TRACK 07 AUDIO
    TITLE Blah Blah Blah
    PERFORMER Rockapella
    INDEX 01 22:51:00
  TRACK 08 AUDIO
    TITLE Stand By Me
    PERFORMER Rockapella
    INDEX 01 25:42:00
  TRACK 09 AUDIO
    TITLE Where Would We Be?
    PERFORMER Rockapella
    INDEX 01 28:56:00
  TRACK 10 AUDIO
    TITLE The Lion Sleeps Tonight
    PERFORMER Rockapella
    INDEX 01 32:09:00
  TRACK 11 AUDIO
    TITLE Up on the Roof/Wonderful World
    PERFORMER Rockapella
    INDEX 01 34:47:00
  TRACK 12 AUDIO
    TITLE Tempted
    PERFORMER Rockapella
    INDEX 01 38:42:00
  TRACK 13 AUDIO
    TITLE People Change
    PERFORMER Rockapella
    INDEX 01 42:17:00
  TRACK 14 AUDIO
    TITLE Use Me
    PERFORMER Rockapella
    INDEX 01 45:58:00
  TRACK 15 AUDIO
    TITLE Dock of the Bay
    PERFORMER Rockapella
    INDEX 01 49:33:00
  TRACK 16 AUDIO
    TITLE Zombie Jamboree
    PERFORMER Rockapella
    INDEX 01 52:57:00
  TRACK 17 AUDIO
    TITLE Keep On Smilin'
    PERFORMER Rockapella
    INDEX 01 56:37:00
  TRACK 18 AUDIO
    TITLE 16 Tons
    PERFORMER Rockapella
    INDEX 01 60:20:00
  TRACK 19 AUDIO
    TITLE Moments Of You
    PERFORMER Rockapella
    INDEX 01 63:17:00
  TRACK 20 AUDIO
    TITLE A Change In My Life
    PERFORMER Rockapella
    INDEX 01 66:16:00
  TRACK 21 AUDIO
    TITLE Long Cool Woman in a Black Dress
    PERFORMER Rockapella
    INDEX 01 71:13:00
```

Note: The timings on this cue sheet don't match the Wikipedia track list
exactly; I had to make a few modifications for the DVD version.

## License

MIT License

Copyright (c) 2017 Kar Epker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[cue sheet]: https://en.wikipedia.org/wiki/Cue_sheet_(computing)
[mp3splt]: https://en.wikipedia.org/wiki/Mp3splt
[rockapella_live_in_concert_cd]: https://en.wikipedia.org/wiki/In_Concert_(Rockapella_album)
