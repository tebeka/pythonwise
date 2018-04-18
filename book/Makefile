book: book.pdf

book.pdf: book-flat.md
	pandoc $< \
	    -V links-as-notes \
	    --toc \
	    --include-in-header header.tex \
	    -t latex \
	    -o $@

book-flat.md: book.md
	awk -f flatten.awk < $< > $@

clean:
	rm -f book.pdf book-flat.md

fresh: clean book

.PHONY: book clean fresh
