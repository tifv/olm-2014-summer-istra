function HighlighLaTeXSpaceErrors()
    highlight latexspaceerror ctermbg=yellow guibg=yellow
    match latexspaceerror /\<\(а\|и\|[Вв]\|[Кк]\|[Сс]\|[Уу]\|[Ии]з\|[Оо]т\|[ДдПпСст]о\|[Зз]а\|[Нн][ае]\|[Ее][еёйю]\|[Оо]н\|[Ии]х\)\zs\( \|\n\)\ze\|\zs\( \|\n\)\ze---\|\zs\( \|\n\)\ze\(ли\|же\|бы\)\>/
endfunction

function SubstituteLaTeXSpaceErrors()
    %substitute/\<\(а\|и\|[Вв]\|[Кк]\|[Сс]\|[Уу]\|[Ии]з\|[Оо]т\|[ДдПпСст]о\|[Зз]а\|[Нн][ае]\|[Ее][еёйю]\|[Оо]н\|[Ии]х\)\zs\( \|\n\)\ze\|\zs\( \|\n\)\ze---\|\zs\( \|\n\)\ze\(ли\|же\|бы\)\>/\~/ce
endfunction

