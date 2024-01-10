# Makefile
srcname = test
cc = gcc

# Default target
all: $(srcname)
	@echo "Finish!"

# Linking stage
$(srcname): $(srcname).o
	@echo "Linking stage: Creating executable '$(srcname)'"
	$(cc) $(srcname).o -o $(srcname)

# Assembly stage
$(srcname).o: $(srcname).s
	@echo "Assembly stage: Creating object file '$(srcname).o'"
	$(cc) -c $(srcname).s -o $(srcname).o

# Compilation stage
$(srcname).s: $(srcname).i
	@echo "Compilation stage: Creating assembly file '$(srcname).s'"
	$(cc) -S $(srcname).i -o $(srcname).s

# Preprocessing stage
$(srcname).i:
	@echo "Preprocessing stage: Creating preprocessed file '$(srcname).i'"
	$(cc) -E $(srcname).c -o $(srcname).i

# Clean target
clean:
	@echo "Cleaning up"
	rm -f $(srcname).i $(srcname).s $(srcname).o $(srcname)
