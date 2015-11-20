`default_nettype none
`include "divider.vh"


//-- Procesador Simplez
module microbio (input wire clk,          //-- Reloj del sistema
                 input wire rstn_ini,     //-- Reset
                 output wire [3:0] leds,  //-- leds
                 output wire stop);       //-- Indicador de stop

//-- Parametro: fichero con el programa a cargar en la rom
parameter ROMFILE = "prog.list";

//-- Parametro: Tiempo de espera para la instruccion WAIT
parameter WAIT_DELAY = `T_200ms;

//-- Codigos de operacion de las instrucciones de simplez
localparam ST   = 3'o0;
localparam LD   = 3'o1;
localparam ADD  = 3'o2;
localparam BR   = 3'o3;
localparam BZ   = 3'o4;
localparam CLR  = 3'o5;
localparam DEC  = 3'o6;
localparam HALT = 3'o7;

//-- Codigos de operacion extendidos
localparam HALTE = 4'hE; //-- Halt extended
localparam WAIT = 4'hF;  //-- Wait

//-- Tamaño de la memoria ROM a instanciar
localparam AW = 9;     //-- Anchura del bus de direcciones
localparam DW = 12;     //-- Anchura del bus de datos

//-- Instanciar la memoria RAM
wire [DW-1: 0] mem_dout;
wire [AW-1: 0] addr;

genrom
  #( .ROMFILE(ROMFILE),
     .AW(AW),
     .DW(DW))
  ROM (
        .clk(clk),
        .addr(addr),
        .data_out(mem_dout)
      );

//-- Registrar la señal de reset
reg rstn = 0;

always @(posedge clk)
  rstn <= rstn_ini;

  //-- Declaracion de las microordenes
  reg cp_inc = 0;   //-- Incrementar contador de programa
  reg cp_load = 0;  //-- Cargar el contador de programa
  reg cp_sel = 0;   //-- Seleccion de la direccion del contador de programa
  reg ri_load = 0;  //-- Cargar el registro de instruccion
  reg halt = 0;     //-- Instruccion halt ejecutada
  reg a_load = 0;   //-- Cargar el acumulador

  //-- Contador de programa
  reg [AW-1: 0] cp;

  always @(posedge clk)
    if (!rstn)
      cp <= 0;
    else if (cp_load)
      cp <= 5;
    else if (cp_inc)
      cp <= cp + 1;


  //-- Multiplexor de acceso a la direccion de memoria
  //-- cp_sel = 1 ---> Se direcciona la memoria desde el CP
  //-- cp_sel = 0 ---> Se direcciona la memoria desde el CD del RI
  assign addr = (cp_sel) ? cp : CD;
  /*always @(*)
    if (cp_sel)
      addr = cp;
    else
      addr = CD;*/


  //-- Registro de instruccion
  reg [DW-1: 0] ri;

  //-- Descomponer la instruccion en los campos CO y CD
  wire [2:0] CO = ri[11:9];  //-- Codigo de operacion
  wire [8:0] CD = ri[8:0];   //-- Campo de direccion
  wire [3:0] COE = ri[11:8]; //-- Código de operacion extendido

  always @(posedge clk)
    if (!rstn)
      ri <= 0;
    else if (ri_load)
      ri <= mem_dout;

//-- Registro de stop
//-- Se pone a 1 cuando se ha ejecutado una instruccion de HALT
reg reg_stop;

always @(posedge clk)
  if (!rstn)
    reg_stop <= 0;
  else if (halt)
    reg_stop <= 1;

//-- Registro acumulador
reg [DW-1:0] reg_a;

always @(posedge clk)
  if (!rstn)
    reg_a <= 0;
  else if (a_load)
    reg_a <= mem_dout;



//-- Debug
assign leds = reg_a[3:0];

//-- Debug
assign stop = reg_stop;


//----------- PERIFERICOS --------
//-- Divisor para marcar la duracion de cada estado del automata
wire clk_tic;

dividerp1 #(WAIT_DELAY)
  TIMER0 (
    .clk(clk),
    .clk_out(clk_tic)
  );


//-------------------- UNIDAD DE CONTROL
localparam INIT = 0;
localparam FETCH = 1;
localparam EXEC1 = 2;
localparam EXEC2 = 3;
localparam END = 4;

//-- Estado del automata
reg [2:0] state;
reg [2:0] next_state;

//-- Transiciones de estados

always @(posedge clk)
  if (!rstn)
    state <= INIT;
  else
    state <= next_state;

//-- Generacion de microordenes
//-- y siguientes estados
always @(*) begin

  //-- Valores por defecto
  next_state = state;      //-- Por defecto permanecer en el mismo estado
  cp_inc = 0;
  cp_load = 0;
  cp_sel = 1;
  ri_load = 0;
  halt = 0;
  a_load = 0;

  case(state)
    //-- Estado inicial
    INIT:
      next_state = FETCH;

    FETCH: begin
      next_state = EXEC1;
      ri_load = 1;
    end

    EXEC1: begin
      case (CO)

        //-- Procesar codigos de operacion extendidos
        HALT: begin

          //-- Instrucciones extendidas
          case (COE)

            //-- Instruccion HALT de simplez
            HALTE: begin
              halt = 1;
              next_state = EXEC1;  //-- Permanecer en el mismo estado... para siempre...
            end

            //-- Instruccion WAIT de microbio
            WAIT: begin
                //-- Mientras no se active clk_tic, se sigue en el mismo
                //-- estado de ejecucion
                if (clk_tic) next_state = END;
                else next_state = EXEC1;
            end

          endcase

        end

        LD: begin
          cp_sel = 0;
          next_state = EXEC2;
        end

      endcase
    end

    EXEC2: begin
      case (CO)
        LD: begin
          a_load = 1;
          next_state = END;
        end
      endcase
    end

    END: begin
      next_state = FETCH;
      cp_inc = 1;
    end

  endcase
end






endmodule
