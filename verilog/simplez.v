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
                output wire [3:0] leds,
                output reg stop
                );

//-- Anchura de los datos: Bus datos, acumulador, RI
parameter DATAW = 12;

//-- Anchura de las direcciones: Bus direciones, CP, RA
parameter ADDRW = 9;

//---------------------------------------------------------------------
//-- RUTA DE DATOS
//---------------------------------------------------------------------

//--------------- Microordenes
reg lec;
reg era;
reg esc;

//-- Para CP
reg incp;
reg ecp;
reg ccp;
reg scp;

//-- Para RI
reg eri;
reg sri;

//-- para AC
reg eac;
reg sac;

//-------- Buses
wire [DATAW-1: 0] busD;   //-- Bus de datos
wire [ADDRW-1: 0] busAi;  //-- Bus de direcciones (interno)

//-------- Registro de direcciones externas
reg [ADDRW-1: 0] RA;

always @(negedge clk)
  if (rstn == 0)
    RA <= 0;
  else if (era)
    RA <= busAi;

//-- Volcar el campo de direccion al bus de direcciones
assign busAi = (sri) ? CD : {ADDRW{1'bz}};


//--------------- Registro de instruccion
reg [DATAW-1: 0] RI;

//-- Formato de las intrucciones
//-- Todas las instrucciones tienen el mismo formato
//--  CO  | CD.    CO de 3 bits.  CD de 9 bits
wire [2:0] CO = RI[11:9];  //-- Codigo de operacion
wire [ADDRW-1: 0] CD = RI[ADDRW-1: 0];   //-- Campo de direccion

always @(negedge clk)
  if (rstn == 0)
    RI <= 0;
  else if (eri)
    RI <= busD;

//---------------- Memoria -------------------------

wire [DATAW-1-4:0] temp; //-- Temp!!!!!

//-- Instanciar la memoria principal
memory
  ROM (
        .clk(clk),
        .addr(12'h0),
        .rd(lec),
        .wr(esc),
        .data_in(busD),
        .data_out(busD)
      );


assign {temp,leds} = busD;

//-----------------------------------------------------------
//-- SECUENCIADOR
//-----------------------------------------------------------

//-- Estados del secuenciador
localparam I0 = 0; //-- Lectura de instruccion. Incremento del PC
localparam I1 = 1; //-- Decodificacion y ejecucion
localparam O0 = 2; //-- Lectura o escritura del operando
localparam O1 = 3; //-- Terminacion del ciclo

//-- Codigos de operacion de las instrucciones
localparam ST   = 3'o0;
localparam LD   = 3'o1;
localparam ADD  = 3'o2;
localparam BR   = 3'o3;
localparam BZ   = 3'o4;
localparam CLR  = 3'o5;
localparam DEC  = 3'o6;
localparam HALT = 3'o7;


//-- Registro de estado
reg [2:0] state;

always @(negedge clk)
  if (rstn == 0)
    state <= I0;  //--Estado inicial: Lectura de instruccion
  else 
    case (state)

      //-- Lectura de instruccion
      //-- Pasar al siguiente estado
      I0: state <= I1;

      //-- Decodificacion de la instruccion
      I1: state <= O0;

      //-- Lectura o escritura del operando
      O0: state <= O1;

      //-- Terminacion de ciclo
      O1: state <= O1;

      default: state <= I0;

    endcase


//-- Generacion de las microordenes
always @* begin

  //--- Valores por defecto de las señales
  //--  (para que no se generen latches)
  lec <= 0;
  eri <= 0;
  sri <= 0;
  era <= 0;
  esc <= 0;
  stop <= 0;

  //-- Cambios en las señales
  case (state)

    //-- Lectura de instruccion
    I0: begin
      lec  <= 1;  //-- Habilitar lectura en memoria
      eri  <= 1;  //-- Capturar la instruccion y meterla en RI
    end

    I1: begin 
      era <= 1; //-- ST: Capturar la direccion donde hacer store
      sri <= 1; //-- ST: Volcar direccion operando en bus Ai
    end

    O0: begin
      esc <= 1; //-- ST: Escritura del dato en memoria
    end

    O1: begin
      stop <= 1;
    end

  endcase
end


endmodule










