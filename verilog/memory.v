module memory(
    output reg [11:0] data_out,
    input [8:0] address,
    input read_enable,
    input clk
);
    reg [11:0] memory [0:511];

    always @(negedge clk) begin
        if (read_enable) begin
            data_out <=memory[address];
        end
    end

    initial begin
      memory[0] = 12'o0400;  //-- ST /400o (Dir. 100h)
      //memory[1] = 12'o7000;  //-- HALT
      //memory[2] = 12'h555;
    end
endmodule
