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

wire [8:0] busAi;

//-- Microordenes
reg era;  //-- Enable registro RA
reg lec;   //-- Lectura de la memoria principal
reg esc;   //-- Escritura en la memoria principal

//-- Microordenaes para el CP
reg ccp;   //-- Clear CP
reg ecp;   //-- Enable CP (para carga)
reg incp;  //-- Incrementar el contador de programa
reg scp;   //-- Activar salida del CP

//-- Microordenes para el de instruccion RI
reg eri;   //-- Enable registro RI
reg sri;   //-- Activar salida del RI

wire [11:0] busD;
wire [11:0] test;



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
//assign busAi = 9'b0_0000_0000; 


//-------------------- Contador de programa
reg [8:0] CP;

always @(negedge clk)
  if (rstn == 0)    //-- Reset (inicio)
    CP <= 'b0;
  //else if (ccp)     //-- Clear
  //  CP <= 'b0;
  //else if (ecp)     //-- Load
  //  CP <= busAi;
  else if (incp)    //-- Incrementar
    CP <= CP + 1;
  

//-- Conexión al bus Ai
assign busAi = scp ? CP : 'bz;

//------------------------------------------------------
//--             Registro de instruccion
//------------------------------------------------------
localparam HALT = 3'o7;
localparam ST = 3'o0;

reg [11:0] RI;

//-- Formato de las intrucciones
//-- Todas las instrucciones tienen el mismo formato
//--  CO  | CD.    CO de 3 bits.  CD de 9 bits
wire [2:0] CO = RI[11:9];  //-- Codigo de operacion
wire [8:0] CD = RI[8:0];   //-- Campo de direccion

always @(negedge clk)
  if (rstn == 0)
    RI <= 0;
  else if (eri)
    RI <= busD;

//-- Conexión al bus Ai
assign busAi = sri ? CD : 'bz;


//-- Hello world! encender el led!
assign LED0 = rstn;

assign dataled = {RI[11], RI[10], RI[9]};

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

//-- OJO!!! SEÑAL ERA esta mal!!!!! comprobar!!!!!

always @*
  case (state)
    I0: begin
      lec <= 1;  //-- Leer en MP
      eri <= 1;  //-- Habilitar registro de instruccion
      incp <= 1; //-- Incrementar contador de programa
      sri <= 0;
      era <= 0;
      esc <= 0;
      ccp <= 0;

      scp <= 0;  //-- Salida del contador programa


      stop <= 0;
      
    end

    I1: begin
      lec <= 0; 
      eri <= 0;
      incp <= 0;
      sri <= 1;  //-- Salida de CD (del RI)
      era <= 1;  //-- Habilitar registro A
      esc <= 0;
      ccp <= 0;
      scp <= 0;
      

      //-- Instruccion HALT
      if (CO == HALT)
        stop <= 1;
      else
        stop <= 0;

    end

    O0: begin
      lec <= 0;
      eri <= 0;
      incp <= 0;
      sri <= 0;
      era <= 0;
      esc <= 1;  //-- Escritura en la memoria

      ccp <= 0;
      
      scp <= 0;

      stop <= 0;
    end

    O1: begin
      lec <= 0;
      eri <= 0;
      incp <= 0;
      sri <= 0;
      era <= 1;
      esc <= 0;

      ccp <= 0;
      
      scp <= 0;

      stop <= 0;
    end

    default: begin
      lec <= 0;
      eri <= 0;
      incp <= 0;
      sri <= 0;
      era <= 0;
      esc <= 0;

      ccp <= 0;
      
      scp <= 0;

      stop <= 0;
    end

  endcase

endmodule







