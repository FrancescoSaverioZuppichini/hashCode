import numpy as np

FILE_PATH = './a_example.in'

with open(FILE_PATH, encoding='utf-8') as file:
    lines = file.readlines()
    raw_data = [line.split(' ') for line in lines]

parser_func = np.vectorize(lambda x: int(x))
data = np.array(raw_data)

data = parser_func(data)

problem = {'rows': data[0, 0],
           'columns': data[0, 1],
           'vehicles': data[0, 2],
           'rides': data[0, 3],
           'bonus': data[0, 4],
           'steps': data[0, 5],
           'data': data[1:, :]
           }

print(problem)


class Ride:
    def __init__(self, id, row):
        self.done = False,
        self.start_pos = row[0:2]
        self.finish_pos = row[2:4]
        self.early_step = row[4]
        self.latest_step = row[-1]


print(Ride(1, problem['data'][0]).__dict__)


class Car:
    def __init__(self, id,simulation):
        self.id = id #car id
        self.pos = None #car position
        self.state = 'f' # o = free, o = occupied
        self.target_pos = None #next position to reach
        self.rides = [] #rides stack
        self.sim = simulation

    def movement(self):
        #check dist == 0
        if np.abs(self.target_pos[0]-self.pos[0])>=np.abs(self.target_pos[1]-self.pos[1]):
            if self.target_pos[0]>self.pos[0]:
                self.pos[0]+=1
            else:
                self.pos[0]-=1# CASO distanza =0 ???
        else:
            if self.target_pos[1]>self.pos[1]:
                self.pos[1]+=1
            else:
                self.pos[1]-=1# CASO distanza =0 ???

    def lifeCycle(self):
        ada=1

