# fasttyper
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
