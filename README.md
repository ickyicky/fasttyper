# fasttyper
[![](https://github.com/ickyicky/fasttyper/blob/main/doc/fasttyper.gif?raw=true)](https://github.com/ickyicky/fasttyper)

# About

_Fasttyper_ is minimalistic typing test based on user provided exercising text. It supports both reading from text files and stdin supporting wide range of usecases. The goal was to create it as simple as it can be, without any additional bloatware functionalities. That means that _Fasttyper_ doesn't come with build in test generator and you have to provide your own scripts generating tests. Some examples of such scrips are providen in [Usage section](#usage).

# Installation

_Fasttyper_ is currently maintained on [TestPyPi](https://test.pypi.org/) Python Package Index. To install package simpply use:

`python3 -m pip install fasttyper`

# Usage

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

To exit program simply complete test or press CTRL+C.

## Example scripts

```sh
function ff() {
	mkdir -p ~/.cache/fasttyper
	local amount="${1:-50}"
	local language="${2:-english}"
	local sfile=~/.cache/fasttyper/$language
	local source_path=https://raw.githubusercontent.com/Miodec/monkeytype/master/static/languages/$language.json
	[[ ! -f $sfile ]] && curl -s $source_path | python3 -c "import sys, json; print('\n'.join(json.load(sys.stdin)['words']))" > $sfile
	shuf -n $amount $sfile | python3 -m fasttyper
}
```
`ff 50 english_1k`

This shell function shuffles N words from cached word list, and if given word list doesnt exist it download's it.
