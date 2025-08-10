# Master Makefile for All Paper Series

# Subdirectories
BERNOULLI_DIR = bernoulli_series
OBLIVIOUS_DIR = oblivious_series
BRIDGE_DIR = bridge_paper

# Default target - build all series
all: bernoulli oblivious bridge
	@echo ""
	@echo "================================================"
	@echo "All paper series built successfully!"
	@echo "================================================"

# Build individual series
bernoulli:
	@echo ""
	@echo "Building Bernoulli Types series..."
	@echo "--------------------------------"
	@$(MAKE) -C $(BERNOULLI_DIR) all

oblivious:
	@echo ""
	@echo "Building Oblivious Computing series..."
	@echo "------------------------------------"
	@$(MAKE) -C $(OBLIVIOUS_DIR) all

bridge:
	@echo ""
	@echo "Building Bridge paper..."
	@echo "----------------------"
	@$(MAKE) -C $(BRIDGE_DIR) all

# Clean targets
clean:
	@echo "Cleaning all auxiliary files..."
	@$(MAKE) -C $(BERNOULLI_DIR) clean
	@$(MAKE) -C $(OBLIVIOUS_DIR) clean
	@$(MAKE) -C $(BRIDGE_DIR) clean

cleanall:
	@echo "Cleaning all files including PDFs..."
	@$(MAKE) -C $(BERNOULLI_DIR) cleanall
	@$(MAKE) -C $(OBLIVIOUS_DIR) cleanall
	@$(MAKE) -C $(BRIDGE_DIR) cleanall

# Rebuild everything
rebuild: cleanall all

# Check all papers for warnings
check:
	@echo "Checking Bernoulli series..."
	@$(MAKE) -C $(BERNOULLI_DIR) check
	@echo ""
	@echo "Checking Oblivious series..."
	@$(MAKE) -C $(OBLIVIOUS_DIR) check
	@echo ""
	@echo "Checking Bridge paper..."
	@$(MAKE) -C $(BRIDGE_DIR) check

# Count pages in all series
pages:
	@echo ""
	@echo "Page counts by series:"
	@echo "====================="
	@echo ""
	@echo "Bernoulli Types Series:"
	@echo "-----------------------"
	@$(MAKE) -C $(BERNOULLI_DIR) pages -s
	@echo ""
	@echo "Oblivious Computing Series:"
	@echo "---------------------------"
	@$(MAKE) -C $(OBLIVIOUS_DIR) pages -s
	@echo ""
	@echo "Bridge Paper:"
	@echo "-------------"
	@$(MAKE) -C $(BRIDGE_DIR) pages -s
	@echo ""

# Quick build targets for individual series
b: bernoulli
o: oblivious
br: bridge

# Help
help:
	@echo "Master Makefile for Paper Series"
	@echo "================================"
	@echo ""
	@echo "Targets:"
	@echo "  all       - Build all paper series (default)"
	@echo "  bernoulli - Build only Bernoulli Types series"
	@echo "  oblivious - Build only Oblivious Computing series"
	@echo "  bridge    - Build only Bridge paper"
	@echo "  clean     - Remove auxiliary files from all series"
	@echo "  cleanall  - Remove all generated files including PDFs"
	@echo "  rebuild   - Clean and rebuild everything"
	@echo "  check     - Check all papers for LaTeX warnings"
	@echo "  pages     - Show page counts for all papers"
	@echo "  help      - Show this help message"
	@echo ""
	@echo "Quick shortcuts:"
	@echo "  b  - Build Bernoulli series"
	@echo "  o  - Build Oblivious series"
	@echo "  br - Build Bridge paper"
	@echo ""
	@echo "For individual paper targets, use:"
	@echo "  make -C bernoulli_series 01  # Build paper 1 of Bernoulli series"
	@echo "  make -C oblivious_series 03  # Build paper 3 of Oblivious series"

.PHONY: all bernoulli oblivious bridge clean cleanall rebuild check pages help b o br