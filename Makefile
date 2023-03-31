.PHONY: all setup run

PYTHON = python3
VENV_DIR = venv
VENV_ACTIVATE = $(VENV_DIR)/bin/activate
SCRIPT = NLP.py

all: setup run

setup: $(VENV_ACTIVATE)

$(VENV_ACTIVATE):
	$(PYTHON) -m venv $(VENV_DIR)
	. $(VENV_ACTIVATE) && pip install -r requirements.txt

run: setup
	. $(VENV_ACTIVATE) && $(PYTHON) $(SCRIPT)
