#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 01:12:40 2024

@author: danyvarghese
"""

from itertools import product
import sys
sys.path.insert(0, '../')
from maze_util import *



import sys
sys.path.insert(0, '../../')
from PyGol_Final_20240718 import  *

# =============================================================================
# Learning From 2*2 Grid using PyGol
# =============================================================================

# =============================================================================
# Example Generation
# =============================================================================
def maze_example_generation(instance = "maze", 
                                input_grid = [], grid_size=2, 
                                blocked_cell = [],
                                max_steps = 2):
    all_one_step_moves = []
    all_two_step_moves = []
    examples = []
    facts = []
    positions = [(i, j) for i, j in product(range(grid_size), repeat=max_steps) 
                 if (i, j) != blocked_cell]
    for start in positions:
        one_step_moves, two_step_moves = generate_moves(start, grid, grid_size)
        all_one_step_moves.extend(one_step_moves)
        all_two_step_moves.extend(two_step_moves)
        
    for idx, move in enumerate(all_one_step_moves):
        bk_ex = "move(a_"+str(idx)+",b_"+str(idx)+")."
        examples.append(bk_ex)
        bk_facts = move[2]+"(a_"+str(idx)+",b_"+str(idx)+")."
        facts.append(bk_facts)
    
    for idx, move in enumerate(all_two_step_moves):
        bk_ex = "move(a_1"+str(idx)+",c_1"+str(idx)+")"
        examples.append(bk_ex)
        bk_facts_1 = move[2]+"(a_1"+str(idx)+",b_1"+str(idx)+")."
        bk_facts_2 = move[3]+"(b_1"+str(idx)+",c_1"+str(idx)+")."
        facts.append(bk_facts_1)
        facts.append(bk_facts_2)
        
    return examples, facts

# =============================================================================
# Input Grid Generation
# Grid size = 2
# =============================================================================
    
grid_size = 2
blocks = []
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    



positive_examples, facts = maze_example_generation(input_grid = grid, 
                            blocked_cell = blocks, grid_size=2)

print(positive_examples)
print(facts)


# =============================================================================
# PyGol Learning Phase
# =============================================================================
print("\n------------ Training Stage Starts ------------")
# Bottom Clause generation

P,N=bottom_clause_generation(file=facts, 
                             positive_example=positive_examples, 
                             negative_example=[], 
                             container="memory", tqdm_disable=True)

# Training data split
Train_P, Test_P, Train_N, Test_N=pygol_train_test_split(test_size=0, 
                                                        positive_file_dictionary=P,
                                                        negative_file_dictionary=N) 

# Learning Phase
model= pygol_learn(Train_P, Train_N, file=[],  
                   max_literals=2, key_size=24, set_chain=True, rule_noise_check=True, tail_recursion=True, eval_metrics=False, verbose=True)

print("\n\t------------- Learned Rules -------------")
print("\t Number of rules:-", len(model.hypothesis))
for i,j in enumerate(model.hypothesis):
    print("\t",i+1,j)
print("\n------------- Training Stage Ends -------------")
# =============================================================================
# PyGol Testing Phase
# =============================================================================

print("\n------------ Testing Stage Starts ------------")


basic_moves, recursive_moves = list_moves(model.hypothesis)


# file names gride size 5
input_files_grid_5 = ["1","2","3","4","5"]

print("\n\t Grid Size:",5)
print(f"\t{'File Name':<10} {'Final Path':<15} {'Total Path (Inc. Back Tracking)':<30}")
print("\t","-" * 55)
for file in input_files_grid_5:
    grid, start, end = load_map_data(file)
    
    path, total_steps = pathfinding(start, end, grid, basic_moves, recursive_moves)
    print(f"\t{file + '.py':<10} {len(path):<15} {total_steps:<30}")

input_files_grid_9 = ["6","7","8","9","10"]

print("\n\t Grid Size:",9)
print(f"\t{'File Name':<10} {'Final Path':<15} {'Total Path (Inc. Back Tracking)':<30}")
print("\t","-" * 55)
for file in input_files_grid_9:
    grid, start, end = load_map_data(file)
    
    path, total_steps = pathfinding(start, end, grid, basic_moves, recursive_moves)
    print(f"\t{file + '.py':<10} {len(path):<15} {total_steps:<30}")

input_files_grid_16 = ["11","12","13","14","15"]

print("\n\t Grid Size:",16)
print(f"\t{'File Name':<10} {'Final Path':<15} {'Total Path (Inc. Back Tracking)':<30}")
print("\t","-" * 55)
for file in input_files_grid_16:
    grid, start, end = load_map_data(file)
    
    path, total_steps = pathfinding(start, end, grid, basic_moves, recursive_moves)
    print(f"\t{file + '.py':<10} {len(path):<15} {total_steps:<30}")
print("\n------------ Testing Stage End ------------")


