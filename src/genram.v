//----------------------------------------------------------------------------
//-- Memoria RAM genérica
//------------------------------------------
//-- (C) BQ. October 2015. Written by Juan Gonzalez (Obijuan)
//-- GPL license
//----------------------------------------------------------------------------
//-- Memoria con los siguientes parametros:
//--  * AW: Numero de bits de las direcciones
//--  * DW: Numero de bits de los datos
//--  * ROMFILE: Fichero a usar para cargar la memoria
//--
//-- Con este componente podemos hacer memorias ram de cualquier tamano
//----------------------------------------------------------------------------

module genram #(             //-- Parametros
         parameter ROMFILE = "",
         parameter AW = 9,   //-- Bits de las direcciones (Adress width)
         parameter DW = 12)   //-- Bits de los datos (Data witdh)

       (        //-- Puertos
         input clk,                      //-- Señal de reloj global
         input cs,                       //-- Chip select
         input wire [AW-1: 0] addr,      //-- Direcciones
         input wire rw,                  //-- Modo lectura (1) o escritura (0)
         input wire [DW-1: 0] data_in,   //-- Dato de entrada
         output reg [DW-1: 0] data_out); //-- Dato a escribir

//-- Parametro: Nombre del fichero con el contenido de la RAM
//parameter ROMFILE = "";

//-- Calcular el numero de posiciones totales de memoria
localparam NPOS = 2 ** AW;

  //-- Memoria
  reg [DW-1: 0] ram [0: NPOS-1];

  //-- Lectura de la memoria
  //-- Solo si el chip select esta activado!
  always @(posedge clk) begin
    if (cs & rw == 1)
        data_out <= ram[addr];
  end

  //-- Escritura en la memoria
  //-- Solo si el chip select esta activado
  always @(posedge clk) begin
    if (cs & rw == 0)
        ram[addr] <= data_in;
  end

//-- Cargar en la memoria el fichero ROMFILE
//-- Los valores deben estan dados en hexadecimal
initial begin
  if (ROMFILE) $readmemh(ROMFILE, ram);
end


endmodule
