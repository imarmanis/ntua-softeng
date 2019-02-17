all: StRS-01.pdf StRS-02.pdf StRS-03.pdf

%.pdf: source/%.tex
	xelatex $<
	$(RM) $*.log $*.aux $*.out

clean:
	$(RM) *.pdf *.log *.aux *.out
