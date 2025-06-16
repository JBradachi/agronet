# Variables
PYTHON := python3
VENV_DIR := venv
REQUIREMENTS := requirements.txt

# Default target
.PHONY: all
all: venv run

# Create virtual environment
$(VENV_DIR)/bin/activate: $(REQUIREMENTS)
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)

# Activate virtual environment
venv: $(VENV_DIR)/bin/activate

# Run the application
run: runbd runcli runser
		
runbd: $(VENV_DIR)/bin/$(PYTHON) ./banco/banco.py
runcli: $(VENV_DIR)/bin/$(PYTHON) ./servidor/listener.py
runser: $(VENV_DIR)/bin/$(PYTHON) ./cliente/interface.py

# Clean up
.PHONY: clean
clean:
	rm -rf $(VENV_DIR)