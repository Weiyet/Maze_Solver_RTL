module MazeSolver #(
    parameter maze_col = 17,
    parameter maze_row = 17,
    parameter start_point_x = 0,
    parameter start_point_y = 0,
    parameter end_point_x = 16,
    parameter end_point_y = 16
)(
    input wire clk,
    input wire rst,
    input wire start,
    input wire [maze_col*maze_row-1:0] maze,
    output wire [maze_col*maze_row-1:0] solution,
    output wire done
);

// Matrix for Maze
wire maze_matrix [maze_row-1:0][maze_col-1:0];
reg visited_matrix [maze_row-1:0][maze_col-1:0];
reg solution_matrix [maze_row-1:0][maze_col-1:0];

// Define position coordinate
reg [clogb2(maze_col)-1:0] curr_x, prev_x;
reg [clogb2(maze_row)-1:0] curr_y, prev_y;
reg track_back_upd;

// Start rising edge detect
reg start_dly;
wire start_rising_edge;

reg [1:0] done_temp;

integer i,j;

genvar k,x;
generate 
    for (k = 0; k < maze_row; k = k + 1) begin
       for (x = 0; x < maze_col; x = x + 1) begin
          assign maze_matrix[k][x] = maze[k*maze_col + x];
       end
    end
endgenerate

always @(posedge clk or posedge rst) begin
    if (rst) begin
        start_dly <= 1'b0;
    end
    else begin
        start_dly <= start;
    end
end

assign start_rising_edge = ~start_dly & start;

always @(posedge clk or posedge rst) begin
    if (rst) begin
        // Reset the maze solver state
        curr_x <= 0;
        curr_y <= 0;
        prev_x <= 0;
        prev_y <= 0;
        track_back_upd <= 0;
    end else if(start_rising_edge) begin 
        curr_x <= start_point_x;
        curr_y <= start_point_y;
    end else if(!start) begin
        curr_x <= 0;
        curr_y <= 0;
        prev_x <= 0;
        prev_y <= 0;
        track_back_upd <= 0;
    end else if(curr_x != end_point_x | curr_y != end_point_y) begin
        prev_x <= curr_x;
        prev_y <= curr_y;
        // Move to the next unvisited and unobstructed neighbor (right, down, left, up)
        // Move right
        if (curr_x < (maze_col - 1) & !visited_matrix[curr_x + 1][curr_y] & maze_matrix[curr_x + 1][curr_y]) begin
            curr_x <= curr_x + 1;
            track_back_upd <= 0;
        // Move down
        end else if (curr_y < (maze_row - 1) & !visited_matrix[curr_x][curr_y + 1] & maze_matrix[curr_x][curr_y + 1]) begin
            curr_y <= curr_y + 1;
            track_back_upd <= 0;
        // Move left
        end else if (curr_x > 0 & !visited_matrix[curr_x - 1][curr_y] & maze_matrix[curr_x - 1][curr_y]) begin
            curr_x <= curr_x - 1;
            track_back_upd <= 0;
        // Move up
        end else if (curr_y > 0 & !visited_matrix[curr_x][curr_y - 1] & maze_matrix[curr_x][curr_y - 1]) begin
            curr_y <= curr_y - 1;
            track_back_upd <= 0;
        // Track back
        end else begin
            track_back_upd <= 1;
            
            // track back right
            if (curr_x < (maze_col - 1) & solution_matrix[curr_x + 1][curr_y])
                curr_x <= curr_x + 1;
            // track back down
            else if (curr_y < (maze_row - 1) & solution_matrix[curr_x][curr_y + 1]) 
                curr_y <= curr_y + 1;
            // track back left
            else if (curr_x > 0 & solution_matrix[curr_x - 1][curr_y]) 
                curr_x <= curr_x - 1;
            // track back up
            else if (curr_y > 0 & solution_matrix[curr_x][curr_y - 1]) 
                curr_y <= curr_y - 1;
            
        end        
    end
end


// solution_matrix
always @(posedge clk or posedge rst) begin
    if (rst) begin
        for (i = 0; i < maze_row; i = i + 1) begin
           for (j = 0; j < maze_col; j = j + 1) begin
              solution_matrix[i][j] <= 1'b0;
           end
        end
    end else if (!start) begin
        for (i = 0; i < maze_row; i = i + 1) begin
           for (j = 0; j < maze_col; j = j + 1) begin
              solution_matrix[i][j] <= 1'b0;
           end
        end
    end else if (track_back_upd) begin
        solution_matrix[prev_x][prev_y] <= 1'b0;
    end else begin
        solution_matrix[curr_x][curr_y] <= 1'b1;
    end
end 

// glue logic for solution stream output
genvar y,z;
generate 
    for (y = 0; y < maze_row; y = y + 1) begin
       for (z = 0; z < maze_col; z = z + 1) begin
          assign solution [y * maze_col + z] = solution_matrix[y][z];
       end
    end
endgenerate


// visited_matrix 
always @(posedge clk or posedge rst) begin
    if (rst) begin
        for (i = 0; i < maze_row; i = i + 1) begin
           for (j = 0; j < maze_col; j = j + 1) begin
              visited_matrix[i][j] <= 1'b0;
           end
        end
    end else if (!start) begin
        for (i = 0; i < maze_row; i = i + 1) begin
           for (j = 0; j < maze_col; j = j + 1) begin
              visited_matrix[i][j] <= 1'b0;
           end
        end
    end 
    else begin
        visited_matrix[curr_x][curr_y] <= 1'b1;
    end
end 

// done 
always @(posedge clk or posedge rst) begin
    if (rst) begin
        done_temp <= 2'b0;
    end
    else if (curr_x == end_point_x && curr_y == end_point_y) begin
        done_temp <= {1'b1,done_temp[1]};
    end
    else if (!start) begin 
        done_temp <= 2'b0;
    end
end

assign done = done_temp[0];

// my verilog simulator does not support synthesizable $clogb2  
function integer clogb2;
    input[31:0] value;
    for(clogb2=0; value>0; clogb2=clogb2+1)
        value = value>>1;
endfunction

endmodule