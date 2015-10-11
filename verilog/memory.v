module rom32x4 (input clk,
                input wire [4:0] addr,
                output reg [3:0] data);

  //-- Memoria
  reg [3:0] rom [0:31];

  always @(negedge clk) begin
    data <= rom[addr];
  end
    

//-- Inicializacion de la memoria. 
//-- Solo se dan valores a las 8 primeras posiciones
//-- El resto permanecera a 0
  initial begin
    rom[0] = 4'h0; 
    rom[1] = 4'h1;
    rom[2] = 4'h2;
    rom[3] = 4'h3;
    rom[4] = 4'h4; 
    rom[5] = 4'h5;
    rom[6] = 4'h6;
    rom[7] = 4'h7;
   end


endmodule



/*


module memory(
    input wire clk,
    input wire [8:0] address,
    input wire read_enable,
    //input wire write_enable,
    //input wire [11:0] data_in,
    output reg [11:0] data_out
);
    reg [11:0] memory [0:511];

    always @(negedge clk) begin
      data_out <= (read_enable) ? memory[address] : {12{1'bz}};

      //if (write_enable) 
      //      memory[address] <= data_in;

    end


    initial begin
      
      memory[0] = 12'o0400;  //-- ST /400o (Dir. 100h)
      memory[1] = 12'o7000;  //-- HALT
      
      memory[2] = 12'o0002;
      memory[3] = 12'o0003;
      memory[4] = 12'o0004;
      memory[5] = 12'o0005;
    end
endmodule


*/
