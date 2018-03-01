import numpy as np

def distance(pos, target):
    return np.abs(pos[0] - target[0]) + np.abs(pos[1] - target[1])

FILE_PATH = './b_should_be_easy.in'

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
        self.rides = [Ride(row, id) for id, row in enumerate(d['data'])]
        self.cars = [Car(c, self) for c in range(self.n_vehicles)]

    def printFra(self):
        smap = [['.'] * self.columns] * self.rows

        for car in self.cars:
            x = car.pos[0]
            y = car.pos[0]
            smap[x][y] = '9'

        for i in range(self.rows):
            for j in range(self.columns):
                print(smap[i][j], end='')
            print('')

    def plan(self):
        schedule = {v: [[0, None]] for k, v in enumerate(self.cars)}

        for ride in self.rides:
            for car in self.cars:
                # print(car.pos)
                if ride.free:

                    car_start_before = float('inf')
                    car_start = None
                    car_total = 0

                    for other_car in self.cars:
                        d_car_to_start = distance(other_car.pos, ride.start_pos)
                        d_start_to_finish = distance(ride.start_pos, ride.finish_pos)
                        d_so_far = schedule[other_car][-1][0]
                        total = d_car_to_start + d_start_to_finish + d_so_far
                        if d_so_far < car_start_before:
                            car_start_before = d_so_far
                            car_start = other_car
                            car_total = total

                    car_start.pos = ride.finish_pos
                    schedule[car_start].append([car_total, ride])
                    ride.free = False

        for k, v in schedule.items():
            schedule[k].pop(0)
            for i in range(len(schedule[k])):
                schedule[k][i] = schedule[k][i][1]
                k.rides = schedule[k]
                k.target= k.rides[0].start_pos


    def run(self,print_map=True):
        self.plan()

        for self.time in range(0, self.steps):
            # print(self.time)
            for car in self.cars:
                # print(car.id)
                car.lifeCycle()

            if print_map:
                self.print()

        print('Final results', self.points, self.solution, sep='\n-----------\n\t')


class Ride:
    def __init__(self, row, id):
        self.id = id
        self.free = True
        self.done = False
        self.start_pos = row[0:2]  # it was 'from'
        self.finish_pos = row[2:4]
        self.early_step = row[4]
        self.latest_step = row[-1]

    def __str__(self):
        return str("({})-({})".format(self.start_pos, self.finish_pos))

class Car:
    def __init__(self, id,simulation):
        self.id = id #car id
        self.pos = np.array([0,0]) #car position
        self.state = 'f' # o = free, o = occupied
        self.target = None #next position to reach
        self.rides = [] #rides stack
        self.sim = simulation

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

sim = Simulation(problem)
sim.run(False)

