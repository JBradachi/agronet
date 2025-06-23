# Variables
# Alvo parão, execute com make -j 4
.PHONY: all
all: subsys_nameserver subsys_bd subsys_ser subsys_cli  

subsys_bd:
	cd banco && $(MAKE)
subsys_cli:
	cd cliente && $(MAKE)
subsys_ser:
	cd servidor && $(MAKE)
subsys_nameserver:
	python3 -m Pyro5.nameserver

# Clean up
.PHONY: clean
clean:
	cd banco && $(MAKE) clean
	cd cliente && $(MAKE) clean
	cd servidor && $(MAKE) clean
