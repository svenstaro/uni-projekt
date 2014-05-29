all: master.pdf

cpustates.ps: images/cpustates.dot
	dot -Teps images/cpustates.dot  -o images/cpustates.eps

%.pdf: %.tex $(wildcard *.tex) calc.s cpustates.ps
	pdflatex -shell-escape $<
	@grep -q 'Rerun to' $(<:.tex=.log) && pdflatex -shell-escape $< || :
	@grep -q 'Rerun to' $(<:.tex=.log) && pdflatex -shell-escape $< || :

.PHONY: show clean
show: master.pdf
	xdg-open $<

clean:
	rm -f *.{out,aux,log,eps,lof,lot,toc} *-eps-converted-to.pdf master.synctex.gz master.pdf images/cpustates.eps

