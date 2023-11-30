function! s:PasteDocTest()
	let indent=getline(".")->matchstr('\v^\s+')
	exec "normal! o\<esc>p0\<c-v>`]I".l:indent."... \<esc>"
	if @+[0] == '^\n'
		normal k dd
	endif
endfunction
nnoremap gV :call <sid>PasteDocTest()<CR>

function! s:Advent(day) abort
	if !(a:day >= 1 && a:day <= 25)
		throw "Invalid day (".a:day.") must be between 1-25"
	endif

	let fname="day_".printf("%02d", a:day).".py"
	if filereadable(l:fname)
		exec "e ".l:fname
	else
		e template.py
		exec "saveas ".l:fname
		exec "H chmod +x ".l:fname
		exec "H clear"
		call TerminalClose()
	endif
endfunction	

command! -nargs=1 Advent :call s:Advent(<args>)
