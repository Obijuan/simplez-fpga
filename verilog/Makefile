#----------------------------------------
#-- Establecer nombre del componente
#----------------------------------------
#-- Folder to store the peripherals
PERIPH = peripherals

NAME = simplez
DEPS = genram.v $(PERIPH)/dividerp1.v $(PERIPH)/uart_tx.v $(PERIPH)/baudgen_tx.v \
                $(PERIPH)/uart_rx.v $(PERIPH)/baudgen_rx.v

#-------------------------------------------------------
#-- Objetivo por defecto: hacer simulacion y sintesis
#-------------------------------------------------------
all: sim sint

prog: sint
	iceprog $(NAME).bin

#----------------------------------------------
#-- make sim
#----------------------------------------------
#-- Objetivo para hacer la simulacion del
#-- banco de pruebas
#----------------------------------------------
sim: $(NAME)_tb.vcd

#-----------------------------------------------
#-  make sint
#-----------------------------------------------
#-  Objetivo para realizar la sintetis completa
#- y dejar el diseno listo para su grabacion en
#- la FPGA
#-----------------------------------------------
sint: $(NAME).bin

#-------------------------------
#-- Compilacion y simulacion
#-------------------------------
$(NAME)_tb.vcd: $(NAME).v $(DEPS) $(NAME)_tb.v prog.list

	#-- Compilar
	iverilog $(NAME).v $(DEPS) $(NAME)_tb.v -o $(NAME)_tb.out

	#-- Simular
	./$(NAME)_tb.out

	#-- Ver visualmente la simulacion con gtkwave
	gtkwave $@ $(NAME)_tb.gtkw &

#------------------------------
#-- Sintesis completa
#------------------------------
$(NAME).bin: $(NAME).pcf $(NAME).v $(DEPS) prog.list

	#-- Sintesis
	yosys -p "synth_ice40 -blif $(NAME).blif" $(NAME).v $(DEPS)

	#-- Place & route
	arachne-pnr -d 1k -p $(NAME).pcf $(NAME).blif -o $(NAME).asc

	#-- Generar binario final, listo para descargar en fgpa
	icepack $(NAME).asc $(NAME).bin



#-- Limpiar todo
clean:
	rm -f *.bin *.asc *.blif *.out *.vcd *~

.PHONY: all clean prog sim

