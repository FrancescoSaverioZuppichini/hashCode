import numpy as np 

FILE_PATH = './a_example.in'

with open(FILE_PATH, encoding='utf-8') as file:
    lines = file.readlines()
    raw_data = [line.split(' ') for line in lines]

    
parser_func = np.vectorize(lambda x: int(x))
data = np.array(raw_data)

data = parser_func(data)

problem = {'rows': data[0,0], 
           'columns': data[0,1], 
           'vehicles': data[0,2], 
           'rides': data[0,3], 
           'bonus': data[0,4], 
           'steps': data[0,5],
           'data': data[1:,:]
          }

print(problem)

class Ride:
    def __init__(self, id, row):
        self.done = False,
        self.start = row[0:2] # it was 'from'
        self.to = row[2:4]
        self.latest = row[4]
        self.finish = row[-1]
        
print(Ride(1, problem['data'][0]).__dict__)

class Car:
    def __init__(self, id):
        self.id = id
        self.pos = None
        self.state = None
        self.target = None
        self.rides = []