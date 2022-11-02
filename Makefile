#set the latex compiler, pure pdflatex cannot handle unicode, so i choose xelatex
tex=xelatex
#the name of the main document to compile (without .pdf / .tex)
job=cheatsheet
#some programs that might be called something else elsewhere
open=xdg-open
copy=cp
remove=rm

src=preamble.tex def.tex lstdef.tex
mat=cheatsheet.py segments.tex
temps=*.aux *.fdb_latexmk *.fls *.log *.out *.synctex.gz *.toc *.nav *.snm *.bbl *.blg *.run.xml *.bcf *.vrb

#uncomment this to make the tex commands not flood you with their output
#texquiet= > /dev/null

default: all

$(job).pdf: $(job).tex $(src) $(mat) Makefile
	$(tex) $< $(texquiet)

cheatbeamer.pdf: cheatbeamer.tex $(src) $(mat) Makefile
	$(tex) $< $(texquiet)

segments.tex: cheatsheet.py segment.py
	./segment.py > segments.tex

.PHONY: all default init clean

all: $(job).pdf cheatbeamer.pdf

init: $(job).tex
	touch $(job).tex
	$(MAKE) $(job).pdf
	$(MAKE) $(job).pdf
	$(open) $(job).pdf

open:
	$(open) $(job).pdf
	$(open) cheatbeamer.pdf

clean:
	$(remove) -f $(temps)
