//-------------------------------------------------------------------
//-- simplez_tb.v
//-- Banco de pruebas para simplez
//-------------------------------------------------------------------
//-- (c) BQ september 2015. Written by Juan Gonzalez (Obijuan)
//-------------------------------------------------------------------
//-- GPL License
//-------------------------------------------------------------------

module simplez_tb();

//-- Registro para generar la señal de reloj
reg clk = 0;

//-- Simulacion de la señal de reset
reg rst = 0;

wire [2:0] dataled;
wire stop;

//-- Instanciar el componente
simplez 
  CPU0 (
    .clk(clk),
    .rstn(rst),
    .dataled(dataled),
    .stop(stop)
  );

//-- Generador de reloj. Periodo 2 unidades
always 
  # 1 clk <= ~clk;


//-- Proceso al inicio
initial begin

  //-- Fichero donde almacenar los resultados
  $dumpfile("simplez_tb.vcd");
  $dumpvars(0, simplez_tb);

  //-- Reset 
  #4 rst <= 0;
  #2 rst <= 1;

  #10 $display("FIN de la simulacion");
  $finish;
end

endmodule

