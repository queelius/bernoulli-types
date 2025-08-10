# Makefile for Bridge Paper

# LaTeX compiler
LATEX = pdflatex
BIBTEX = bibtex
FLAGS = -interaction=nonstopmode -halt-on-error

# Paper file
PAPER = bridge_hash_bernoulli_oblivious
PDF = $(PAPER).pdf

# Default target
all: $(PDF)

# Build the paper
$(PDF): $(PAPER).tex references.bib
	@echo "Building $(PDF)..."
	@$(LATEX) $(FLAGS) $(PAPER) > /dev/null 2>&1 || (echo "LaTeX failed"; exit 1)
	@$(BIBTEX) $(PAPER) > /dev/null 2>&1 || true
	@$(LATEX) $(FLAGS) $(PAPER) > /dev/null 2>&1
	@$(LATEX) $(FLAGS) $(PAPER) > /dev/null 2>&1
	@echo "Successfully built $(PDF)"

# Clean auxiliary files
clean:
	@echo "Cleaning auxiliary files..."
	@rm -f *.aux *.log *.bbl *.blg *.out *.toc *.lof *.lot *.nav *.snm *.vrb *.fls *.fdb_latexmk *.synctex.gz 2>/dev/null || true

# Clean everything including PDF
cleanall: clean
	@echo "Cleaning PDF file..."
	@rm -f $(PDF) 2>/dev/null || true

# Rebuild
rebuild: cleanall all

# Check for warnings
check:
	@echo "Checking for LaTeX warnings..."
	@if [ -f $(PAPER).log ]; then \
		grep -i "warning" $(PAPER).log | grep -v "Font Warning" || echo "No warnings found"; \
	fi

# Count pages
pages:
	@if [ -f $(PDF) ]; then \
		pages=$$(pdfinfo $(PDF) 2>/dev/null | grep Pages | awk '{print $$2}'); \
		echo "$(PDF): $$pages pages"; \
	else \
		echo "PDF not found. Run 'make' first."; \
	fi

# Help
help:
	@echo "Bridge Paper - Makefile targets:"
	@echo ""
	@echo "  all      - Build the paper (default)"
	@echo "  clean    - Remove auxiliary files"
	@echo "  cleanall - Remove auxiliary files and PDF"
	@echo "  rebuild  - Clean and rebuild"
	@echo "  check    - Check for LaTeX warnings"
	@echo "  pages    - Count pages in PDF"
	@echo "  help     - Show this help message"

.PHONY: all clean cleanall rebuild check pages help