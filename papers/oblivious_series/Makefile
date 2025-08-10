# Makefile for Oblivious Computing Paper Series

# LaTeX compiler
LATEX = pdflatex
BIBTEX = bibtex
FLAGS = -interaction=nonstopmode -halt-on-error

# Paper files
PAPERS = 01_foundations_oblivious_computing \
         02_secure_indexes_oblivious_bernoulli \
         03_oblivious_data_structures \
         04_cipher_boolean_rings \
         05_private_information_retrieval \
         06_applications_systems \
         oblivious_addendum_uniform_encoding

# Output files
PDFS = $(PAPERS:=.pdf)

# Default target
all: $(PDFS)

# Pattern rule for building PDFs
%.pdf: %.tex unified_notation_oblivious.tex references.bib
	@echo "Building $@..."
	@$(LATEX) $(FLAGS) $< > /dev/null 2>&1 || (echo "LaTeX failed on $<"; exit 1)
	@if grep -q "\\\\bibliography" $<; then \
		$(BIBTEX) $* > /dev/null 2>&1 || true; \
		$(LATEX) $(FLAGS) $< > /dev/null 2>&1; \
		$(LATEX) $(FLAGS) $< > /dev/null 2>&1; \
	fi
	@echo "Successfully built $@"

# Individual paper targets
01: 01_foundations_oblivious_computing.pdf
02: 02_secure_indexes_oblivious_bernoulli.pdf
03: 03_oblivious_data_structures.pdf
04: 04_cipher_boolean_rings.pdf
05: 05_private_information_retrieval.pdf
06: 06_applications_systems.pdf
addendum: oblivious_addendum_uniform_encoding.pdf

# Clean targets
clean:
	@echo "Cleaning auxiliary files..."
	@rm -f *.aux *.log *.bbl *.blg *.out *.toc *.lof *.lot *.nav *.snm *.vrb 2>/dev/null || true

cleanall: clean
	@echo "Cleaning PDF files..."
	@rm -f $(PDFS) 2>/dev/null || true

# Rebuild everything
rebuild: cleanall all

# Check for missing citations or references
check:
	@echo "Checking for LaTeX warnings..."
	@for paper in $(PAPERS); do \
		if [ -f $$paper.log ]; then \
			grep -i "warning" $$paper.log | grep -v "Font Warning" || true; \
		fi \
	done

# Count pages
pages:
	@echo "Page counts:"
	@for pdf in $(PDFS); do \
		if [ -f $$pdf ]; then \
			pages=$$(pdfinfo $$pdf 2>/dev/null | grep Pages | awk '{print $$2}'); \
			printf "%-45s %3s pages\n" "$$pdf:" "$$pages"; \
		fi \
	done
	@if ls *.pdf >/dev/null 2>&1; then \
		total=$$(pdfinfo *.pdf 2>/dev/null | grep Pages | awk '{sum += $$2} END {print sum}'); \
		echo "----------------------------------------"; \
		printf "%-45s %3s pages\n" "Total:" "$$total"; \
	fi

# Help target
help:
	@echo "Oblivious Computing Paper Series - Makefile targets:"
	@echo ""
	@echo "  all      - Build all papers (default)"
	@echo "  01-06    - Build individual paper by number"
	@echo "  addendum - Build the uniform encoding addendum"
	@echo "  clean    - Remove auxiliary files"
	@echo "  cleanall - Remove auxiliary files and PDFs"
	@echo "  rebuild  - Clean and rebuild everything"
	@echo "  check    - Check for LaTeX warnings"
	@echo "  pages    - Count pages in all PDFs"
	@echo "  help     - Show this help message"

.PHONY: all clean cleanall rebuild check pages help 01 02 03 04 05 06 addendum