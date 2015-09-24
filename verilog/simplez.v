//---------------------------------------------------------------------------
//-- Implementacion del procesador docente SIMPLEZ en verilog
//-- Diseñado para ser sintetizado usando las herramientas libres del 
//-- proyecto icestorm:  http://www.clifford.at/icestorm/
//--
//----------------------------------------------------------------------------
//-- Simplez es una cpu clásica, con la memoria y los periféricos situados
//-- "fuera del chip". Sin embargo, en esta implementación se tomará el 
//-- enfoque de convertir simplez en un "microcontrolador", que disponga en 
//-- su interior de memoria y periféricos
//----------------------------------------------------------------------------
//-- (C) BQ, september 2015. Written by Juan Gonzalez Gomez (Obijuan)
//-- Released under the GPL license
//----------------------------------------------------------------------------
`default_nettype none

module simplez (input wire clk,
                input wire rstn,
                output wire LED0,
                output wire [3:0] dataled
                );

wire [8:0] busAi;

//-- Microordenes
wire era;  //-- Enable registro RA
reg eri;  //-- Enable registro RI
reg incp; //-- Incrementar el contador de programa
reg lec;  //-- Lectura de la memoria principal

wire [11:0] busD;

//-- Registro RA
reg [8:0] RA;

//-- Capturar la direccion que hay en el bus A SOLO si la
//-- microorden era esta activa
always @(negedge clk)
  if (rstn == 0)
    RA <= 0;
  else if (era)
    RA <= busAi;


//-- Cablear la direccion 0 al bus de direcciones
assign busAi = 9'b0_0000_0000; 


//-- Contador de programa
reg [8:0] CP;

always @(negedge clk)
  if (rstn == 0)
    CP <= 0;
  else if (incp)
    CP <= CP + 1;

//-- Registro de instruccion
reg [11:0] RI;

always @(negedge clk)
  if (rstn == 0)
    RI <= 0;
  else if (eri)
    RI <= busD;


//-- Hello world! encender el led!
assign LED0 = rstn;

assign era = 0;

assign dataled = {1'b0, RI[11], RI[10], RI[9]};


//-- Memoria
memory 
  MP(
     .clk(clk),
     .data_out(busD),
     .address(RA),
     .read_enable(lec)
     );

//-- Secuenciador
localparam I0 = 0; //-- Lectura de instruccion. Incremento del PC
localparam I1 = 1; //-- Decodificacion y ejecucion
localparam O0 = 2; //-- Lectura o escritura del operando
localparam O1 = 3; //-- Terminacion del ciclo

reg [1:0] state;

always @(negedge clk)
  if (rstn == 0)
    state <= I0;  //--Estado inicial: Lectura de instruccion
  else 
    case (state)

      //-- Lectura de instruccion
      //-- Pasar al siguiente estado
      I0: state <= I1;

      //-- Decodificacion de la instruccion
      I1: state <= I1;
    endcase

always @*
  case (state)
    I0: begin
      lec <= 1;  //-- Leer en MP
      eri <= 1;  //-- Habilitar registro de instruccion
      incp <= 1; //-- Incrementar contador de programa
    end

    I1: begin
      lec <= 0; 
      eri <= 0;
      incp <= 0;
    end

    default: begin
      lec <= 0;
      eri <= 0;
      incp <= 0;
    end

  endcase

endmodule






module memory(
    output reg [11:0] data_out,
    input [8:0] address,
    input read_enable,
    input clk
);
    reg [11:0] memory [0:511];

    always @(negedge clk) begin
        if (read_enable) begin
            data_out <=memory[address];
        end
    end

    initial begin
      memory[0] = 12'o7000;  //-- HALT
      memory[1] = 12'h555;
    end
endmodule





