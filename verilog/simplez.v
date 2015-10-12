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

//-- ALU
reg tra2;
reg sum;

//-- Registro para monitorizar
reg [3:0] leds_r;

//-------- Buses
wire [DATAW-1: 0] busD;   //-- Bus de datos
wire [ADDRW-1: 0] busAi;  //-- Bus de direcciones (interno)

//-- Inicializador
//reg rstn = 0;
//always @(negedge clk)
//  rstn <= 1;

//--------------------- Contador de programa ------------------------
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

//----------- ACCESO AL BUS DE DIRECCIONES Ai --------------------
//assign busAi = (sri) ? CD : {ADDRW{1'bz}};
assign busAi = (scp) ? CP :             //-- Sacar CP 
               (sri) ? CD :             //-- Sacar CD del RI
                       {ADDRW{1'b1}};   //-- valor por defecto


//-------- Registro de direcciones externas
reg [ADDRW-1: 0] RA;

always @(negedge clk)
  if (rstn == 0)
    RA <= 0;
  else if (era)
    RA <= busAi;



//-------- Registro de instruccion
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

//-- Monitorizar CO
/*
always @(negedge clk)
  leds_r <= {1'b0, CO};

assign leds = leds_r;
*/


//---------------- Registro acumulador ---------------------------------
reg [DATAW-1: 0] AC;

always @(negedge clk)
  if (rstn == 0)
    AC <= 0;
  else if (eac)
    AC <= alu_out;

//-- Si hubiese soporte de puertas tri-estado, la conexion del acumulador
//-- al bus de datos seria:
//assign busD = (sac) ? AC : {DATAW{1'bz}};
//-- Como no lo hay , esta conexion se hace mas adelante, en el elemento:
//-- ACCESO AL BUS DE DATOS

//----------- Unidad aritmetico logica
wire [DATAW-1: 0] op1;
wire [DATAW-1: 0] op2;

wire [DATAW-1: 0] alu_out;

assign op1 = AC;
assign op2 = busD;

assign alu_out = (tra2) ? op2 :        //-- Obtener operando 2
                 (sum)  ? op1 + op2 :  //-- Suma
                          0;

//-- Instanciar la memoria principal
memory
  ROM (
        .clk(clk),
        .addr(RA),
        .wr(esc),
        .data_in(busD),
        .data_out(data_out)
      );

wire [11:0] data_out;

//------------------ Perifericos
wire cs_leds;

assign cs_leds = (RA == 9'o100) ? 1 : 0;

always @(negedge clk)
  if (rstn == 0)
    leds_r <= 0;
  else if (cs_leds && esc == 1)
    leds_r <= {1'b0 ,busD[2:0]};

assign leds = leds_r;

//-------- ACCESO AL BUS DE DATOS ----------------------------
assign busD =  (sac) ? AC :          //-- conectar el acumulador
                       data_out;     //-- Conectar la memoria


/*
//-- Monitorizar bus de datos
always @(negedge clk)
  leds_r <= busD[3:0];

*/


//-----------------------------------------------------------
//-- SECUENCIADOR
//-----------------------------------------------------------

//-- Estados del secuenciador
localparam INI = 0; //-- Estado de inicializacion
localparam I0 = 1;  //-- Lectura de instruccion. Incremento del PC
localparam I1 = 2;  //-- Decodificacion y ejecucion
localparam O0 = 3;  //-- Lectura o escritura del operando
localparam O1 = 4;  //-- Terminacion del ciclo

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

//-- Transiciones entre los estados
always @(negedge clk)

  if (rstn == 0)
    state <= INI;  //--Estado inicial: Lectura de instruccion

  else begin
    //-- Estado por defecto
    state <= INI;
    case (state)

      //-- Estado inicial
      INI: state <= I0;

      //-- Fetch
      I0: state <= I1;

      //-- Decodificacion de la instruccion
      I1: case (CO)
            //-- Instruccion Halt: permanecer en este estado
            //-- Se dejan de ejecutar instrucciones
            HALT: state <= I1;

            default:
              state <= O0;
          endcase 

      //-- Lectura del operando
      O0: state <= O1;

      //-- Terminacion de ciclo
      O1: state <= INI;
        
    endcase
  end

//-- Asignacion de las microordenes, segun el estado
always @* begin

  //-- Por defecto todas las microordenes a 0
  {lec, eri, incp} <= {1'b0, 1'b0, 1'b0};
  {sri, era, esc}  <= {1'b0, 1'b0, 1'b0};
  {tra2, sac, eac} <= {1'b0, 1'b0, 1'b0};
  scp <= 0;
  stop <= 0;
  sum <= 0;

  case (state)

    INI:  {eri, scp} <= {1'b1, 1'b1};

    I0: {lec, eri, incp} <= {1'b1, 1'b1, 1'b1};

    I1: begin
      {sri, era} <= {1'b1, 1'b1};
      case (CO)
        HALT: begin 
          stop <= 1;
        end
      endcase
    end

    O0:
      case (CO)
        LD:  lec <= 1;
        ST: {esc, sac} <= {1'b1, 1'b1};
      endcase

    O1: begin
      {era, scp} <= {1'b1, 1'b1};
      case (CO)
        ST: sac <= 1;
        LD: {tra2, eac} <= {1'b1, 1'b1};
        ADD: {sum, eac} <= {1'b1, 1'b1};
      endcase
    end

  endcase
end

endmodule










