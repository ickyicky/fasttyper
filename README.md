# fasttyper
[![](https://github.com/ickyicky/fasttyper/blob/main/doc/demo.gif?raw=true)](https://github.com/ickyicky/fasttyper)

# About

_Fasttyper_ is minimalistic typing test based on user provided exercising text. It supports both reading from text files and stdin supporting wide range of usecases. The goal was to create it as simple as it can be, without any additional bloatware functionalities. That means that _Fasttyper_ doesn't come with build in test generator and you have to provide your own scripts generating tests. Some examples of such scrips are providen in [Usage section](#usage).

# Installation

_Fasttyper_ is currently maintained on [PyPi](https://pypi.org/) Python Package Index. To install package simpply use:

`python3 -m pip install fasttyper`

# Usage

With installation of fasttyper you should have new executable - `fasttyper`. It takes two optional positional arguments, amount of words and language (like in [Monkeytype's](https://github.com/Miodec/monkeytype): english, english_1k etc). Default amount of words is 25 and language is english. To run fasttyper simply call:

```bash
fasttyper
```

from command line. There are some avalibe options:

```
usage: fasttyper [-h] [--config FILE] [--unclutter-backspace] [--no-cursor] [amount] [language]

positional arguments:
  amount                Amount of words
  language              Language

options:
  -h, --help            show this help message and exit
  --config FILE, -c FILE
                        configuration file
  --unclutter-backspace, -b
                        unclutter backspace, when it raises ctrl+backspace instead
  --no-cursor, -n       disable cursos
```

I personally use alias:

```
alias ff='fasttyper -n`
```

because i don't like having cursor and i am too lazy to type fasttyper so i just type ff :)

# Running next test and stopping application

To abandon test and start brand new one, press TAB.

To kill application (exit) press CTRL+C.

# Configuring

Fasttyper by default looks for config file in: `$HOME/.config/fasttyper/config.json`. You can provide different location for config file with `--config` argument, for example: `--config=~/.fasttyper.json`. Config has to be a json dict. Avalibe keys:

- **user_input_valid_color** - integer, terminal color for valid text, by default it is 3
- **user_input_invalid_color** - integer, terminal color for invalid text, by default it is 2
- **reference_text_color** - integer, terminal color for reference text, by default it is 8
- **stats_color** - integer, terminal color for stats text, by default it is 5
- **summary_datafile** - datafile storing all stats, by default it is ~/.cache/fasttyper/datafile.csv
- **top_margin_percentage** - integer, percentage of screen used for top margin, by default 30
- **left_margin_percentage** - integer, percentage of screen used for left (and right) margin, by default 10
- **lines_on_screen** - integer, number of lines to display on screen, by default 3

Example config file with all default values in avalibe [here](https://github.com/ickyicky/fasttyper/blob/main/doc/example_config.json).

Other example config files:

```json
{"top_margin_percentage": 40, "left_margin_percentage": 25}
```

```json
{"user_input_valid_color": 5}
```

# Usage as module, piping stuff, custom scripts etc

_Fasttyper_ is ran as an python module, so to execute it simply type:

`python3 -m fasttyper`

from cloned github repository, if you didn't [install](#installation) package from TestPyPi. 

_Fasttyper_ can open text files, which path should be provided as first and only argument to the module execution, for example:

`python3 -m fasttyper example_text.txt`

Program also allows user to pipe text into it. Keep in mind, it only supports spaces and new line characters, so you won't be able to table tabs. For example, you can run _Fasttyper_ on fortune generated quote changing tabulators to spaces with sed:

`furtune | python3 -m fasttyper`

or if you want to randomize words from given file with shuf on for example all disctionaries in system:

`shuf -n5 /usr/share/dict/* | python -m fasttyper`

You can use another similar projects set of words as well, for example to create test with 20 random words from [Monkeytype's](https://github.com/Miodec/monkeytype) english 100 dictionary use:

`curl -s https://raw.githubusercontent.com/Miodec/monkeytype/master/static/languages/english.json | python3 -c "import sys, json; print('\n'.join(json.load(sys.stdin)['words']))" | shuf -n20 | python3 -m fasttyper`

To exit you can either finish test, use `KeyboardInterrupt` (CTRL+C) or tap **tab**. After you finish test, there will be summary printed, use enter to exit from it.

# When backspace does wierd shiet

Some terminal emulators send different values for key presses of backspace and ctrl+backspace. To fix it, simply add `b` flag like that: `python3 -m fasttyper -b`.

# Hiding cursor

To hide the cursor, simply add `n` flag like that: `python3 -m fasttyper -n`.

## Example scripts

```sh
function ff() {
	mkdir -p ~/.cache/fasttyper
	local amount="${1:-50}"
	local language="${2:-english}"
	local sfile=~/.cache/fasttyper/$language
	local source_path=https://raw.githubusercontent.com/Miodec/monkeytype/master/static/languages/$language.json
	[[ ! -f $sfile ]] && curl -s $source_path | python3 -c "import sys, json; print('\n'.join(json.load(sys.stdin)['words']))" > $sfile
	while true
	do
		shuf -n $amount $sfile | python3 -m fasttyper || break
	done
}
```
`ff 50 english_1k`

This shell function shuffles N words from cached word list, and if given word list doesnt exist it download's it. It runs in loop, but does exit from it if you exit fasttyper with CTRL+C.

The above script is avalible for download from doc folder.
