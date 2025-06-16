# Variables
# Alvo parão, execute com make -j 3
.PHONY: all
all: subsys_bd subsys_cli subsys_ser

subsys_bd: 
	cd banco && $(MAKE)
subsys_cli: 
	cd cliente && $(MAKE)
subsys_ser: 
	cd servidor && $(MAKE)

# Clean up
.PHONY: clean
clean:
	cd banco && $(MAKE) clean
	cd cliente && $(MAKE) clean
	cd servidor && $(MAKE) clean