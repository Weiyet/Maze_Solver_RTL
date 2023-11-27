# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0
# Simple tests for an adder module
import random
import asyncio
import copy
import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock
from maze_solver import solve_maze_matrix
from maze_generator import generate_maze_matrix

async def generate_clock(dut):
    dut.clk.value = 1
    while(1):
        await Timer(50, units="ns")
        dut.clk.value = not dut.clk.value

@cocotb.test()
async def maze_solver_randomised_test(dut):
    await cocotb.start(generate_clock(dut))
    maze_rows = 17
    maze_cols = 17
    start_point = (0,0)
    end_point = (maze_rows - 1, maze_cols - 1)
    dut.rst.value = 1
    await Timer(1000, units="ns")
    dut.rst.value = 0

    for i in range(20):
        maze = generate_maze_matrix(maze_rows,maze_cols,start_point,end_point)
        maze_temp = copy.deepcopy(maze)
        solution = solve_maze_matrix(maze_temp,start_point,end_point)
        stream_maze_input = 0
        # for i in maze:
        #      print(i)
        # print("==============")
        # for i in solution:
        #     print(i)
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                stream_maze_input = stream_maze_input + maze[i][j] * 2**(i*len(maze[0]) + j)
        dut.maze.value = stream_maze_input
        await RisingEdge(dut.clk)
        await Timer(5, units="ns")
        dut.start.value = 1
        # big endian to little endian
        maze_dut_input = str(dut.maze.value)[::-1]
        dut._log.info("Maze sent to DUT:")
        for i in range(len(maze)):
            dut._log.info("         "+maze_dut_input[i*len(maze[0]):(i+1)*len(maze[0])])
        await RisingEdge(dut.done)
        dut._log.info("====================================================")
        # big endian to little endian
        solution_dut_output = str(dut.solution.value)[::-1]
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                assert solution_dut_output[i*len(maze[0])+j] == str(solution[i][j]), f"solution is incorrect"
        dut._log.info("Solution received from DUT:")

        for i in range(len(maze)):
            dut._log.info("         "+solution_dut_output[i*len(maze[0]):(i+1)*len(maze[0])])
        dut._log.info("====================================================")
        await RisingEdge(dut.clk)
        dut.start.value = 0
        await Timer(500, units="ns")

    
@cocotb.test()
async def maze_solver_basic_test(dut):
    await cocotb.start(generate_clock(dut))
    maze_rows = 17
    maze_cols = 17
    start_point = (0, 0)
    end_point = (maze_rows - 1, maze_cols - 1)
    maze = [[1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0],
            [0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0],
            [0,0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0],
            [0,0,0,1,1,1,0,1,0,0,0,0,1,0,0,0,0],
            [0,0,0,0,0,1,0,1,0,0,0,0,1,1,0,0,0],
            [0,0,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0],
            [0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0],
            [0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,0],
            [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1],
            [0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1],
            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1]]
    solution =[[1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]]
    stream_maze_input = 0
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            stream_maze_input = stream_maze_input + maze[i][j] * 2**(i*len(maze[0]) + j)
    dut.maze.value = stream_maze_input
    dut.rst.value = 1
    await Timer(1000, units="ns")
    dut.rst.value = 0
    await Timer(400, units="ns")
    await RisingEdge(dut.clk)
    await Timer(5, units="ns")
    dut.start.value = 1
    # big endian to little endian
    maze_dut_input = str(dut.maze.value)[::-1]
    dut._log.info("Maze sent to DUT:")
    for i in range(len(maze)):
          dut._log.info("         "+maze_dut_input[i*len(maze[0]):(i+1)*len(maze[0])])
    await RisingEdge(dut.done)
    dut._log.info("====================================================")
    # big endian to little endian
    solution_dut_output = str(dut.solution.value)[::-1]
    for i in range(len(maze)):
         for j in range(len(maze[0])):
              assert solution_dut_output[i*len(maze[0])+j] == str(solution[i][j]), f"solution is incorrect"
    dut._log.info("Solution received from DUT:")

    for i in range(len(maze)):
        dut._log.info("         "+solution_dut_output[i*len(maze[0]):(i+1)*len(maze[0])])
    dut._log.info("====================================================")

    await RisingEdge(dut.clk)
    dut.start.value = 0
    await Timer(500, units="ns")

    