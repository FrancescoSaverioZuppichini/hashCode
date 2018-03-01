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


class Simulation:

    def __init__(self, d):
        self.rows = d['rows']
        self.columns = d['columns']
        self.n_vehicles = d['vehicles']
        self.n_rides = d['rides']
        self.bonus = d['bonus']
        self.steps = d['steps']
        self.solution = []
        self.points = 0

        self.time = 0
        self.rides = [Ride(r, r) for r in range(self.n_rides)]
        self.cars = [Car(c) for c in range(self.n_vehicles)]

    def print(self):
        smap = [['.'] * self.columns] * self.rows

        for car in self.cars:
            x = car.pos[0]
            y = car.pos[0]
            smap[x][y] = self.state

        for i in range(self.rows):
            for j in range(self.columns):
                print(smap[i][j], end='')
            print('')

    def run(self,print_map=True):
        for self.time in range(0, self.steps):
            for car in self.cars:
                car.step()

            if print_map:
                self.print()

        print('Final results', self.points, self.solution, sep='\n-----------\n\t')


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


    def free(self):
        if self.sim.time == self.rides[0].early_step:
            self.state = 'o'
            self.target = self.rides[0].latest_step
        else:
            px = self.pos[0]
            py = self.pos[1]
            tx = self.target[0]
            ty = self.target[1]

            if px > tx:
                self.pos[0] -= 1
            elif px < tx:
                self.pos[0] += 1
            elif py > ty:
                self.pos[1] -= 1
            else:
                self.pos[1] += 1


    def lifeCycle(self):
        px = self.pos[0]
        py = self.pos[1]
        tx = self.target[0]
        ty = self.target[1]

        if px > tx:
            self.pos[0] -= 1
        elif px < tx:
            self.pos[0] += 1
        elif py > ty:
            self.pos[1] -= 1
        elif py < ty:
            self.pos[1] += 1
        else: # same place as target
            if self.state == 'o':
                self.state = 'f'
                self.rides.pop()

                self.target = self.rides[0].start_pos
                if self.pos == self.target:
                    self.free()
                else:
                    tx = self.target[0]
                    ty = self.target[1]

                    if px > tx:
                        self.pos[0] -= 1
                    elif px < tx:
                        self.pos[0] += 1
                    elif py > ty:
                        self.pos[1] -= 1
                    else: # py < ty:
                        self.pos[1] += 1
            else:
                self.free()
#
sim= Simulation()
sim.run()