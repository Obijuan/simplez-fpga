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
                output wire [2:0] dataled,
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

//-- Para CP
reg incp;
reg ecp;
reg ccp;
reg scp;

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


//--------------- Registro de instruccion
reg [DATAW-1: 0] RI;

//-- Formato de las intrucciones
//-- Todas las instrucciones tienen el mismo formato
//--  CO  | CD.    CO de 3 bits.  CD de 9 bits
wire [2:0] CO = RI[11:9];  //-- Codigo de operacion
wire [8:0] CD = RI[8:0];   //-- Campo de direccion

always @(negedge clk)
  if (rstn == 0)
    RI <= 0;
  else
    RI <= busD;


//--------------- Contador de programa
reg [ADDRW-1: 0] CP;

always @(negedge clk)
  if (rstn == 0)
    CP <= 0;

  //-- Incrementar contador programa
  else if (incp)
    CP <= CP + 1;

  //-- Cargar el contador programa
  else if (ecp)
    CP <= busAi;

  //-- Poner a cero contador de programa
  else if (ccp)
    CP <= 0;

//-- Conectar el contador de programa al bus de direcciones interno
assign busAi = (scp) ? CP : {ADDRW{1'bz}};

//---------------- Memoria 
memory 
  MP(
     .clk(clk),
     .data_out(busD),
     .address(RA),
     .read_enable(lec)
     );


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
      I1:
        case(CO)
          HALT: state <= I1;
          ST: state <= O0;

          default: state <= I1;
        endcase

      //-- Lectura o escritura del operando
      O0: state <= O1;

      //-- Terminacion de ciclo
      O1: state <= I0;

      default: state <= I0;

    endcase


//-- Generacion de las microordenes
always @*
  case (state)
    I0: begin
      lec  <= 1;
      incp <= 1;
      era  <= 0;
      scp  <= 0;
      ecp  <= 0;
      ccp  <= 0;

      stop  <= 0;
    end

    I1: begin
      lec  <= 0;
      incp <= 0;
      era  <= 1;
      scp  <= 0;
      ecp  <= 0;  //-- Depende de BZ (poner a 1)
      ccp  <= 0;  //-- Depende de HALT (Poner a 1)
      stop <= 1;  //-- Depende de HALT (poner a 1)
    end

    O0: begin
      lec  <= 0;
      incp <= 0;
      era  <= 0;
      scp  <= 0;
      ecp  <= 0;
      ccp  <= 0;
      stop <= 0;
    end

    O1: begin
      lec  <= 0;
      incp <= 0;
      era  <= 1;
      scp  <= 1;
      ecp  <= 0;
      ccp  <= 0;
      stop <= 0;
    end

    //-- Para evitar latches
    default: begin
      lec  <= 0;
      incp <= 0;
      era  <= 0;
      scp  <= 0;
      ecp  <= 0;
      ccp  <= 0;
      stop <= 0;
    end

  endcase



endmodule










