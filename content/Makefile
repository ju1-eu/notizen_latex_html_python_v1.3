# LaTeX
# sudo tlmgr update --self
# sudo tlmgr update --all
# Makefile to compile all .tex files in the directory using xelatex/lualatex/pdflatex and biber
# Engines: pdflatex, xelatex, lualatex
# make
# make ENGINE=xelatex
# make ENGINE=lualatex
# make clean
# make clean-pdf

# LaTeX engine choice: pdflatex (default), xelatex, lualatex
ENGINE ?= pdflatex

# Find all .tex files in the directory
TEX_FILES := $(wildcard *.tex)

# Convert .tex filenames to .pdf
PDFS := $(TEX_FILES:.tex=.pdf)

# Rule to make all PDFs
all: $(PDFS)

# Rule to convert a .tex file to .pdf using the selected engine and biber
%.pdf: %.tex
ifeq ($(ENGINE),xelatex)
	xelatex $<
	biber $(basename $<)
	xelatex $<
	xelatex $<
else ifeq ($(ENGINE),lualatex)
	lualatex $<
	biber $(basename $<)
	lualatex $<
	lualatex $<
else
	pdflatex $<
	biber $(basename $<)
	pdflatex $<
	pdflatex $<
endif

# Clean target to remove generated non-PDF files
clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.run.xml *.bcf *.fls

# New target to remove PDF files
clean-pdf:
	rm -f $(PDFS)

# PHONY targets
.PHONY: all clean clean-pdf
