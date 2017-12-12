//------------------------------------------------------------------------------
//-- Procesador SIMPLEZ F:   Implementacion del procesador SIMPLEZ de Gregorio //-- Fernandez en FPGA, mediante lenguaje Verilog
//------------------------------------------------------------------------------
//-- (C) 2015-2017, Juan Gonzalez-Gomez (Obijuan)
//-----------------------------------------------------------------------------
//-- Released under the LGPL v3 License
//------------------------------------------------------------------------------
`default_nettype none

//-- Procesador Simplez
module simplez_main  (
           input wire clk,          //-- Reloj del sistema
           input wire dtr,          //-- Señal DTR del PC
           input wire sw2,          //-- Pulsador 2
           output wire [7:0] leds,  //-- leds
           output wire stop,        //-- Indicador de stop
           output wire tx,          //-- Salida serie para la pantalla
           input wire rx            //-- Entrada serie del teclado
);

//-- Procesador simplez, con reset conectado
simplez
P0 (clk,
    ~sw2 & dtr,    //-- Reset mediante pulsador o DTR (PC)
    leds,
    stop,
    tx,
    rx
);

endmodule
