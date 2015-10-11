module memory(
    input wire clk,
    input wire [8:0] address,
    input wire read_enable,
    output reg [11:0] data_out
);
    reg [11:0] memory [0:511];

    always @(negedge clk) begin
      data_out <= (read_enable) ? memory[address] : 'bz;
    end


    initial begin
      memory[0] = 12'o0400;  //-- ST /400o (Dir. 100h)
      memory[1] = 12'o7000;  //-- HALT
      memory[2] = 12'h555;
    end
endmodule
