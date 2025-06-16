PYTHON := python3
VENV_DIR := venv
REQUIREMENTS := requirements.txt

# Alvo padrão
.PHONY: all
all: venv runser

# Cria um ambiente virtual
$(VENV_DIR)/bin/activate: $(REQUIREMENTS)
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)

# Ativa o ambiente
venv: $(VENV_DIR)/bin/activate

runser: 
	$(VENV_DIR)/bin/$(PYTHON) listener.py

# Limpa 
.PHONY: clean
clean:
	rm -rf $(VENV_DIR)