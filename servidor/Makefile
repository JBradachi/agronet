PYTHON := python3
VENV_DIR := venv
REQUIREMENTS := requirements.txt

# Default target
.PHONY: all
all: venv runser

# Create virtual environment
$(VENV_DIR)/bin/activate: $(REQUIREMENTS)
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)

# Activate virtual environment
venv: $(VENV_DIR)/bin/activate

runser: 
	$(VENV_DIR)/bin/$(PYTHON) listener.py

# Clean up
.PHONY: clean
clean:
	rm -rf $(VENV_DIR)