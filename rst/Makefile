%.html: %.txt
	rst2html.py --stylesheet style.css $< $@

%.pdf: %.tex
	pdflatex $<

%.tex: %.txt
	rst2latex.py $< $@

all: hw.html hw.pdf

clean:
	rm -f *.aux *.log *.pdf *.html *.out

fresh: clean all

.PHONY: all clean fresh
