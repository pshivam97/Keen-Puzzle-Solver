import json
from z3 import *


def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii')
    return dict(map(ascii_encode, pair) for pair in data.items())

inpfile = "inputs/1.json"

with open(inpfile) as readfile :
    a = readfile.read()

a = a.strip()
data = json.loads(a,object_hook=ascii_encode_dict)


column_indices = ["a",'b','c','d','e','f']
row_indices = [ str(i) for i in range(1,7)]
s = Solver()
board = [ [None for i in range(6)] for j in range(6)]
for i in range(6) :
    for j in range(6) :

        board[i][j] = Int(column_indices[i]+row_indices[j])
        s.add(board[i][j]>0)
        s.add(board[i][j]<7)

# for i in range(6) :
#     for j in range(6) :
#         for k in range(6) :
#             s.add(board[i][j] != board[i][k])
            
# for i in range(6) :
#     for j in range(6) :
#         for k in range(6) :
#             s.add(board[k][i] != board[j][i])

distinct_rows = [ Distinct([ board[i][j] for i in range(6) ])  for j in range(6) ]
distinct_cols   = [ Distinct(board[i]) for i in range(6) ]
s.add(distinct_rows+distinct_cols)

for i in data :
    operator = i[1][-1]
    value = i[1][:len(i[1]) - 1]
    
    if not operator in ["/","-"] :
        expression = []
        for j in i[0] :
            expression.append("board[%d][%d]"%(column_indices.index(j[0]),row_indices.index(j[1])))
            expression.append(operator)

        expression.pop()
        expression = " ".join(expression)
        expression += " == " + value
        expression = eval(expression)

    else :
        i = i[0]
        expression = "Or(board[%d][%d]"%(column_indices.index(i[0][0]),row_indices.index(i[0][1]))
        expression += operator
        expression +=  "board[%d][%d] "%(column_indices.index(i[1][0]),row_indices.index(i[1][1]))
        expression += " == " + value +", "
        expression += "board[%d][%d]"%(column_indices.index(i[1][0]),row_indices.index(i[1][1]))
        expression += operator
        expression +=  "board[%d][%d] == %s )"%(column_indices.index(i[0][0]),row_indices.index(i[0][1]),value)
        expression = eval(expression)


    s.add(expression)


if s.check() == sat :
    m = s.model()
    print m