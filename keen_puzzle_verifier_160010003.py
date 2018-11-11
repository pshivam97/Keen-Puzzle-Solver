### Shivam Pandey
### CS-228 : Logic in CS | Assignment-2 | Keen Puzzle Solver & Verifier

#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/Downloads/z3-4.7.1-x64-osx-10.11.6/bin
#export PYTHONPATH=~/Downloads/z3-4.7.1-x64-osx-10.11.6/bin/python

### Code for INPUT GENERATOR
# for each_line in open("a2-input-raw4"):
#     x = each_line.split()
#     str = '\t\t[["'
#     for t in x[:-1]:
#         if t == x[-2]:
#             str = str + t
#         else:
#             str = str + t + '", "'
#     str = str + '"], "'+x[-1]+'"],'
#     print(str)
#
# a1 a2 3/
# b1 b2 2-
# c1 c2 6*
# d1 e1 6+
# d2 e2 5+
# f1 f2 8+
# a3 a4 15*
# b3 b4 2/
# c3 c4 1-
# d3 d4 12*
# e3 f3 2/
# e4 f4 6*
# a5 a6 5+
# b5 b6 2-
# c5 d5 2/
# c6 d6 2-
# e5 f5 1-
# e6 f6 6*

import json
from z3 import *

input_file = "input_160010003.json"
solution_file = "output.txt"
result = str()
resultList = list()

with open(input_file) as readfile_1 :
    input_file_as_string = readfile_1.read()

solution_list = list()

with open(solution_file) as readfile_2 :
    solution = readfile_2.readline().strip()
    while solution != "" :
        solution = list(solution.lstrip('[').rstrip(']'))
        solution_list.append(solution)
        solution = readfile_2.readline().strip()

input_file_as_string = input_file_as_string.strip()
boards_list = json.loads(input_file_as_string)

column_indices = ['a','b','c','d','e','f']
row_indices = ['1','2','3','4','5','6']

stringToCellDict = dict()

for each_board, each_solution in zip(boards_list,solution_list) :

    solver_machine = Solver()

    board = [[None for i in range(6)] for j in range(6)] ## Initializing the board

    for i in range(6) :
        for j in range(6) :

            board[i][j] = Int(column_indices[i]+row_indices[j])
            solver_machine.add(board[i][j]>0)
            solver_machine.add(board[i][j]<7)

    for i in column_indices :
        for j in row_indices :
            stringToCellDict[i+j] = board[column_indices.index(i)][int(j)-1]

    for i in range(len(solution)) :
        x = i%6
        y = int(i/6)
        solver_machine.add(board[x][y] == each_solution[i])

    for i in range(6) :
        for j in range(5) :
            for k in range(j+1,6) :
                solver_machine.add(board[i][j] != board[i][k])

    for i in range(6) :
        for j in range(5) :
            for k in range(j+1,6) :
                solver_machine.add(board[j][i] != board[k][i])

    for each_constraint in each_board :
        operator = each_constraint[1][-1]
        value = int(each_constraint[1][:len(each_constraint[1]) - 1])

        if operator not in ["/","-"] :
            if operator == '+' :
                i = column_indices.index(each_constraint[0][0][0])
                j = row_indices.index(each_constraint[0][0][1])
                math_expression = board[i][j]

                for each_cell in range(1,len(each_constraint[0])) :
                    i = column_indices.index(each_constraint[0][each_cell][0])
                    j = row_indices.index(each_constraint[0][each_cell][1])
                    math_expression += board[i][j]
                solver_machine.add(math_expression == value)

            else :
                i = column_indices.index(each_constraint[0][0][0])
                j = row_indices.index(each_constraint[0][0][1])
                math_expression = board[i][j]

                for each_cell in range(1,len(each_constraint[0])) :
                    i = column_indices.index(each_constraint[0][each_cell][0])
                    j = row_indices.index(each_constraint[0][each_cell][1])
                    math_expression *= board[i][j]
                solver_machine.add(math_expression == value)
        else :
            if operator == '/' :
                i1 = column_indices.index(each_constraint[0][0][0])
                i2 = column_indices.index(each_constraint[0][1][0])
                j1 = row_indices.index(each_constraint[0][0][1])
                j2 = row_indices.index(each_constraint[0][1][1])
                solver_machine.add(Or(board[i1][j1]/board[i2][j2]==value,board[i2][j2]/board[i1][j1] == value))
            else :
                i1 = column_indices.index(each_constraint[0][0][0])
                i2 = column_indices.index(each_constraint[0][1][0])
                j1 = row_indices.index(each_constraint[0][0][1])
                j2 = row_indices.index(each_constraint[0][1][1])
                solver_machine.add(Or(board[i1][j1] - board[i2][j2]==value,board[i2][j2] - board[i1][j1] == value))

    if solver_machine.check() == sat and len(each_solution) != 0 :
        print("TRUE")
    elif solver_machine.check() == unsat and len(each_solution) == 0:
        print("TRUE")
    else :
        print("FALSE")
