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

time: $(NAME).rpt

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
$(NAME).blif: $(NAME).pcf $(NAME).v $(DEPS) prog.list

	#-- Sintesis
	yosys -p "synth_ice40 -blif $(NAME).blif" $(NAME).v $(DEPS)

#--
%.asc: $(NAME).pcf %.blif
	arachne-pnr -d 1k -o $@ -p $^

#-- Realizar el analis del tiempo
%.rpt: %.asc
	icetime -mtr $@ $<

# -- Generar el bitstream binario
%.bin: %.asc
	icepack $< $@

#-- Limpiar todo
clean:
	rm -f *.bin *.asc *.blif *.out *.vcd *~ *.rpt

.PHONY: all clean prog sim time sint
