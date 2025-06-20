
import sys
sys.path.insert(0, '../')
from maze_util import *



import sys
sys.path.insert(0, '../../')
from PyGol_Final_20240718 import  *


def generate_possible_positions(start, end):
    # Original start and end
    x1, y1 = start
    x2, y2 = end

    # 1. Reversed start and end positions
    reversed_start = end
    reversed_end = start

    diff_x = int(abs(x2-x1)/2)
    diff_y = int(abs(y2-y1)/2)

    alt_start1 = (x1, y2+diff_y)  
    alt_end1 = (x2+10, y2) 
    
    alt_start2 =(x2+10, y2) 
    alt_end2 = (x1, y2+diff_y)  
    
    return [ (start,end),
        (start,end),
        (alt_start1, alt_end1),
        (reversed_start, reversed_end),
        (alt_start2,alt_end2)
        
       
    ]


def obstacle_avoidance_examples(file=[],step=10, train_file=[]):
    Examples = []
    Facts =[]
    start_coords, end_coords = extract_start_end_coordinates(file,step)
    grid, start, end = load_map_data(train_file,cordinates=False)
    possible_positions=generate_possible_positions(start_coords,end_coords)
    for j,i in enumerate(possible_positions):
        
        start=i[0]
        end = i[1]
        path, directions, total_steps = pathgeneration(start, end, grid)
        facts, dirn, example = print_path_and_steps_example(path, total_steps, idx=j)
        Examples.append(example)
        for f in facts:
            Facts.append(f)
    return Facts, Examples
        
       

folder_path = "Episode4"
step=10
train_file = "occ_grid_2_free"
    
# Generate the filename by concatenating the folder name with 'ACTIONS'
actions_file = find_actions_file(folder_path)

BK, examples = obstacle_avoidance_examples(file= actions_file, train_file=train_file)
print("\n------------ Training Stage Starts ------------")
# Bottom Clause generation
P,N = bottom_clause_generation(file=BK,
                               positive_example=examples, 
                               negative_example=[], 
                               container="memory", tqdm_disable=True)
# Training data split
Train_P, Test_P, Train_N, Test_N=pygol_train_test_split(test_size=0, positive_file_dictionary=P, negative_file_dictionary=N)
# Learning Phase
rules = pygol_learn_FSA(Train_P)
print("\n\t------------- Learned Rules -------------")
print("\t Number of rules:-", len(rules))
for i,j in enumerate(rules):
    print("\t",i+1,j)
print("\n------------- Training Stage Ends -------------")
# =============================================================================
# PyGol Testing Phase
# =============================================================================

print("\n------------ Testing Stage Starts ------------")
basic_moves, recursive_moves = list_moves(rules)
 

input_files_episode_10 = ["occ_grid_west_north","occ_grid_west_south",
                      "occ_grid_middle_north", "occ_grid_middle_south",
                      "occ_grid_east_north", "occ_grid_east_south"]

print("\n\t Episode:",10)
print(f"\t{'File Name':<25} {'Final Path':<15} {'Total Path (Inc. Back Tracking)':<30}")
print("\t","-" * 55)
folder_path = "Episode10"
for file in input_files_episode_10:
    grid, _, _ = load_map_data(file, cordinates=False)
    actions_file = find_actions_file(folder_path)
    start_coords, end_coords = extract_start_end_coordinates(actions_file,step)
    
    path, total_steps = pathfinding(start_coords, end_coords, grid, basic_moves, recursive_moves)
    
    print(f"\t{file :<25} {len(path):<15} {total_steps:<30}")


input_files_episode_6 = ["occ_grid_west_north","occ_grid_west_south",
                      "occ_grid_middle_north", "occ_grid_middle_south",
                      "occ_grid_east_north", "occ_grid_east_south"]

print("\n\t Episode:",6)
print(f"\t{'File Name':<25} {'Final Path':<15} {'Total Path (Inc. Back Tracking)':<30}")
print("\t","-" * 55)
folder_path = "Episode6"
for file in input_files_episode_6:
    grid, _, _ = load_map_data(file, cordinates=False)
    actions_file = find_actions_file(folder_path)
    start_coords, end_coords = extract_start_end_coordinates(actions_file,step)
    
    path, total_steps = pathfinding(start_coords, end_coords, grid, basic_moves, recursive_moves)
    print(path)
    print(f"\t{file:<25} {len(path):<15} {total_steps:<30}")


input_files_episode_18 = ["occ_grid_1","occ_grid_1a",
                      "occ_grid_1b", "occ_grid_1c",
                      "occ_grid_1d", "occ_grid_1e"]

print("\n\t Episode:",18)
print(f"\t{'File Name':<25} {'Final Path':<15} {'Total Path (Inc. Back Tracking)':<30}")
print("\t","-" * 55)
folder_path = "Episode18"
for file in input_files_episode_18:
    grid, _, _ = load_map_data(file, cordinates=False)
    actions_file = find_actions_file(folder_path)
    start_coords, end_coords = extract_start_end_coordinates(actions_file,step)
    
    path, total_steps = pathfinding(start_coords, end_coords, grid, basic_moves, recursive_moves)
    
    print(f"\t{file :<25} {len(path):<15} {total_steps:<30}")
print("\n------------ Testing Stage End ------------")







"""
Final=[]
for i in possible_positions:
    
    start=i[0]
    end = i[1]
    print(start,end)
    path, directions, total_steps = pathgeneration(start, end, grid)
   
    facts, dirn, example = print_path_and_steps_example(path, total_steps, idx=1)
    

    P,N = bottom_clause_generation(file=facts, positive_example=[example], negative_example=[], container="memory", tqdm_disable=True)
    
    Train_P, Test_P, Train_N, Test_N=pygol_train_test_split(test_size=0, positive_file_dictionary=P, negative_file_dictionary=N)
    rules = pygol_learn_FSA(Train_P)
    for j in rules:
            if j not in Final:
                Final.append(j)

for i in Final:
    print(i)
"""
"""list_1 =  [76,108,74,74,74,74,209,225,209,219,209,251,278,270,280,300,272,268]
print(len(list_1))

l1=[185,49,65,54,65,60,138,188,145,183,143,180,79,79,146,137,115,180]
print(len(l1))

l2=[65,51,56,56,56,56,56,175,175,178,175,177,171,165,151,146,145,141,144]
print(len(l2))"""
    

print(rules)