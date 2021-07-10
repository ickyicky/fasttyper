# fasttyper
[![](https://github.com/ickyicky/fasttyper/blob/main/doc/example.png?raw=true)](https://github.com/ickyicky/fasttyper)

# About

_Fasttyper_ is minimalistic typing test based on user provided exercising text. It supports both reading from text files and stdin supporting wide range of usecases.

# Usage

_Fasttyper_ is ran as an python module, so to execute it simply type:

`python3 -m fasttyper`

from cloned github repository. Without any argument program waits for user to enter text manually and then signal the end of it with keyboard interrupt (CTRL+C). _Fasttyper_ can open text files, which path should be provided as first and only argument to the module execution, for example:

`python3 -m fasttyper example_text.txt`

Program also allows user to pipe text into it. Keep in mind, it only supports spaces and new line characters, so you won't be able to table tabs. For example, you can run _Fasttyper_ on rfurtune generated quote changing tabulators to spaces with sed:

`rfurtune | sed 's/\t/ /g' | python3 -m fasttyper`

# Known issues

_Fasttyper_ relies on curses library, so in order to allow it to first read piped text and then read characters from terminal users have to exec:

`exec 3<&0`

in their terminal before piping text to _Fasttyper_, duplicating stdin to descriptor 3.
