all: master.pdf

%.pdf: %.tex $(wildcard *.tex)
	pdflatex -shell-escape $<
	@grep 'Rerun to' $(<:.tex=.log) && pdflatex -shell-escape $< || :
	@grep 'Rerun to' $(<:.tex=.log) && pdflatex -shell-escape $< || :

.PHONY: show clean
show: master.pdf
	xdg-open $<

clean:
	rm -f *.{out,aux,log,eps,lof,lot,toc} *-eps-converted-to.pdf master.pdf
