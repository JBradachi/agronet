PYTHON := python3
VENV_DIR := venv
REQUIREMENTS := requirements.txt

# Alvo padrão
.PHONY: all
all: venv runbd

# Cria um ambiente virtual
$(VENV_DIR)/bin/activate: $(REQUIREMENTS)
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)

# Ativa o ambiente
venv: $(VENV_DIR)/bin/activate

runbd: 
	$(VENV_DIR)/bin/$(PYTHON) main.py

# Limpa 
.PHONY: clean
clean:
	rm -rf $(VENV_DIR)