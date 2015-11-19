//-------------------------------------------------------------------
//-- microbio_tb
//-- Banco de pruebas para el microprocesador MICROBIO
//-------------------------------------------------------------------
//-- BQ November 2015. Written by Juan Gonzalez (Obijuan)
//-------------------------------------------------------------------

module simplez_tb();

//-- Programa en codigo maquina a cargar en la rom
parameter ROMFILE = "prog.list";

//-- Registro para generar la señal de reloj
reg clk = 0;

//-- Datos de salida del componente
wire [3:0] leds;
wire stop;
reg rstn = 0;

//-- Instanciar el componente
microbio #(.ROMFILE(ROMFILE))
  dut(
    .clk(clk),
    .rstn_ini(rstn),
    .leds(leds),
    .stop(stop)
  );

//-- Generador de reloj. Periodo 2 unidades
always #1 clk = ~clk;


//-- Proceso al inicio
initial begin

  //-- Fichero donde almacenar los resultados
  $dumpfile("simplez_tb.vcd");
  $dumpvars(0, simplez_tb);

  #2 rstn <= 1;

  # 160 $display("FIN de la simulacion");
  $finish;
end

endmodule
