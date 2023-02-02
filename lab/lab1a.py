import picar_4wd as fc
import random
import time
from queue import PriorityQueue
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt

speed = 10

X = 0
Y = 0
DIR = 'N'
DIR_RIGHT_TRANSFORMATION = {'N' : 'E', 'E' : 'S', 'S' : 'W', 'W' : 'N'}

MOVE = {
    'N' : {
        'l' : (-1, 1), 
        'f' : (0, 1),
        'r' : (1, 1)
    },
    'E' : {
        'l' : (1, 1), 
        'f' : (1, 0),
        'r' : (1, -1)
    },
    'S' : {
        'l' : (1, -1), 
        'f' : (0, -1),
        'r' : (-1, -1)
    },
    'W' : {
        'l' : (-1, -1), 
        'f' : (-1, 0),
        'r' : (-1, 1)
    },
}

turn_time = 1.3

graph = {}

# class Direction(Enum):
#     N = ()

def move_forward():
    fc.forward(speed)
    time.sleep(1.3)
    fc.stop()

def turn_left():
    fc.turn_left(speed)
    time.sleep(turn_time)
    fc.stop()

def turn_right():
    fc.turn_right(speed)
    time.sleep(turn_time)
    fc.stop()
    DIR = DIR_RIGHT_TRANSFORMATION[DIR]


def moveBack():
    fc.backward(speed)
    for i in range(1):
        time.sleep(0.5)
		
# left is negative right is positive
def turn(t):
    if t < 0:
        fc.turn_left(speed)
    else:
        fc.turn_right(speed)
        
    time.sleep(abs(t))
    
def scan_environment():
    current_angle = -90
    fc.get_distance_at(current_angle)
    time.sleep(0.2)

    dist_list = []
    while True:
        dist = fc.get_distance_at(current_angle)
        dist_list.append(dist)
        if current_angle == 90:
            break
        current_angle += 5
    
    fc.get_distance_at(0)
    time.sleep(0.2)

    dist_list = np.array(dist_list)
    print(dist_list)
    angle_list = np.array([i for i in range(0, 181, 5)])
    
    ind = (dist_list > 35) & (dist_list < 0)
    dist_list[ind] = np.inf
    
    return dist_list, angle_list


def get_xy_coord(dist, angle):
    x = np.cos(angle * np.pi / 180) * dist
    y = np.sin(angle * np.pi / 180) * dist
    return x, y

def can_forward():
    dist_list, angle_list = scan_environment() 
    print(dist_list)
    x, y = get_xy_coord(dist_list, angle_list)
    print(x)
    
    l = not np.any(dist_list[0:12] <= 15)
    m = not np.any(dist_list[12:25] <= 15)
    r = not np.any(dist_list[25:37] <= 15)
    return m
    # return [l & m, m, r & m]
    
def add_pair(pair1, pair2):
    return (pair1[0] + pair2[0], pair1[1] + pair2[1])

def sub_pair(pair1, pair2):
    return (pair1[0] - pair2[0], pair1[1] - pair2[1])

def euclidean_dist(curr, dest):
    return np.sqrt((dest[0] - curr[0]) ** 2 + (dest[1] - curr[1]) ** 2)

def a_star(dest):
    X = 0
    Y = 0

    pq = PriorityQueue()
    pq.put((0, (X, Y)))

    while not pq.empty():
        curr = pq.get()

        change = sub_pair(curr[1], tuple([X, Y]))
        print(change)

        if change != (0, 0):
            while MOVE[DIR]['f'] != change:
                turn_right()
            move_forward()
        
        print("hello")

        X = curr[1][0]
        Y = curr[1][1]

        if tuple([X, Y]) == dest:
            break
        
        for _ in range(4):
            move_f = can_forward()
            if move_f:
                new_pair = add_pair(curr[1], MOVE[DIR]['f'])
                pq.put((euclidean_dist(new_pair, dest), new_pair)) 
            turn_right()
    

        
        







if __name__ == "__main__":
    try:
        a_star((0, 3))
    finally:
        fc.stop()


    # turn_right()

    # dist_list, angle_list = scan_environment() 
    # x, y = get_xy_coord(dist_list, angle_list)
    # print(dist_list)
    # print(angle_list)
    # plt.scatter(x, y)
    # plt.show()
    # try: 
    #     main()
    # finally: 
    #     fc.stop()
        







# def main():
#     while True:
#         scan_list = fc.scan_step(35)
#         print(scan_list)
# """
#         if not scan_list:
#             continue
        
#         print(scan_list)
#         tmp = scan_list[3:7]
#         print(tmp)
        
#         if tmp != [2,2,2,2]:
#             moveBack()
#             turnPatter(x, y)
#     plt.show()ra = random.randint(-3, 1)
#             if turnPara == 0:
#                 turnPara = 1
#             turn(turnPara/5)
#         else:
#             fc.forward(speed)
# """


        
"""
def sign(x):
    if x < 0:
        return -1
    else:
        return 1


def main():
    turnPara = 0

    while True:
        scan_list = fc.scan_step(40)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        print(tmp)
        
        if tmp != [2,2,2,2]:
            moveBack()
            while tmp != [2,2,2,2]:
                turnPara = -sign(turnPara) * (abs(turnPara) + 0.2)
                turn(turnPara)
                scan_list = fc.scan_step(40)
                if not scan_list:
                    continue
                tmp = scan_list[3:7]
        else:
            turnPara = 0
            fc.forward(speed)
"""
