module memory (input clk,
               input wire [8:0] addr,
               input wire wr,
               input wire [11:0] data_in,
               output reg [11:0] data_out);

  //-- Memoria
  reg [11:0] mem [0:511];

  always @(negedge clk) begin
    data_out <= mem[addr];

    if (wr) 
      mem[addr] <= data_in;

  end
    

  initial begin
     mem[0] = 12'o1006;    //-- LD
     //mem[1] = 12'o7000;  //-- HALT
     mem[1] = 12'o2007;    //-- ADD
     mem[2] = 12'o2007;    //-- ADD
     //mem[4] = 12'o0100;  //-- ST
     mem[3] = 12'o7000;  //-- HALT
      
     
     mem[6] = 12'o0003;
     mem[7] = 12'o0001;
     
     mem[8] = 12'o0001;  //-- Octal: 10
   end


endmodule


