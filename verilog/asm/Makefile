#----------------------------------------------------------------
#-- Ejemplo de ensamblar y descargar un programa en simplez-F
#----------------------------------------------------------------
NAME = boot_04_count

all: $(NAME).list


%.list: $(NAME).asm
	../sasm.py $^ -o $@

prog: $(NAME).list
	../sboot.py $^


#-- Limpiar todo
clean:
	rm -f *.list

.PHONY: all clean prog
