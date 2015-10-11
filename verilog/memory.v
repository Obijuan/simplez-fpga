module memory (input clk,
               input wire [8:0] addr,
               input wire rd,
               output reg [11:0] data_out);

  //-- Memoria
  reg [11:0] mem [0:511];

  always @(negedge clk) begin
    data_out <= (rd) ? mem[addr] : {12{1'bz}};
  end
    

  initial begin
     mem[0] = 12'o0403;  //-- ST
     mem[1] = 12'o7000;  //-- HALT
      
     mem[2] = 12'o0002;
     mem[3] = 12'o0003;
     mem[4] = 12'o0004;
     mem[5] = 12'o0005;
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
