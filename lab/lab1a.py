import picar_4wd as fc
import random
import time
from queue import PriorityQueue
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt

speed = 10

DIR = 'N'
DIR_RIGHT_TRANSFORMATION = {'N' : 'E', 'E' : 'S', 'S' : 'W', 'W' : 'N'}
DIR_LEFT_TRANSFORMATION = {'N' : 'W', 'E' : 'N', 'S' : 'E', 'W' : 'S'}

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

turn_time = 1.33

graph = {}

def move_forward():
    global DIR
    fc.forward(speed)
    if DIR == 'E': 
        time.sleep(0.3)
    time.sleep(1.2)
    fc.stop()

def turn_left():
    print("turn_left")
    global DIR
    fc.turn_left(speed)
    time.sleep(turn_time+0.2)
    fc.stop()
    DIR = DIR_LEFT_TRANSFORMATION[DIR]

def turn_right():
    print("turn_right")
    global DIR
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
    angle_list = np.array([i for i in range(0, 181, 5)])
    
    return dist_list, angle_list


def get_xy_coord(dist, angle):
    x = np.cos(angle * np.pi / 180) * dist
    y = np.sin(angle * np.pi / 180) * dist
    return x, y

def can_forward():
    global DIR
    dist_list, angle_list = scan_environment() 
    x, y = get_xy_coord(dist_list, angle_list)
    
    l = not np.any(dist_list[0:12] <= 35)
    m = not np.any((dist_list[12:25] <= 35) & (dist_list[12:25] > 0))
    r = not np.any(dist_list[25:37] <= 35)
    print("DIR:", DIR, "can_forward m:", dist_list[12:25])
    return m
    # return [l & m, m, r & m]
    
def add_pair(pair1, pair2):
    return (pair1[0] + pair2[0], pair1[1] + pair2[1])

def sub_pair(pair1, pair2):
    return (pair1[0] - pair2[0], pair1[1] - pair2[1])

def euclidean_dist(curr, dest):
    return np.sqrt((dest[0] - curr[0]) ** 2 + (dest[1] - curr[1]) ** 2)

def exploration_order(curr, dest):
    dx = dest[0] - curr[0]
    dy = dest[1] - curr[1]

    if dx == 0 and dy > 0:
        return ['N', 'E', 'S', 'W']
    elif dx == 0 and dy < 0:
        return ['S', 'W', 'N', 'E'] 
    elif dx > 0 and dy == 0:
        return ['E', 'S', 'W', 'N']
    elif dx < 0 and dy == 0:
        return ['W', 'N', 'E', 'S']

    if dx > 0 and dy > 0:
        return ['N', 'E', 'S', 'W']
    elif dx > 0 and dy < 0:
        return ['E', 'S', 'W', 'N']
    elif dx < 0 and dy > 0:
        return ['W', 'N', 'E', 'S']
    else:
        return ['S', 'W', 'N', 'E'] 

def change_dir(curr, dest):
    print("change_dir:", curr, dest)
    if dest == 'N':
        if curr == 'W':
            turn_right()
        elif curr == 'E':
            turn_left()
        elif curr == 'S':
            turn_right()
            turn_right()
    elif dest == 'E':
        if curr == 'S':
            turn_left()
        elif curr == 'N':
            turn_right()
        elif curr == 'W':
            turn_right()
            turn_right()
    elif dest == 'W':
        if curr == 'N':
            turn_left()
        elif curr == 'S':
            turn_right()
        elif curr == 'E':
            turn_right()
            turn_right()
    else:
        if curr == 'E':
            turn_right()
        elif curr == 'W':
            turn_left()
        elif curr == 'N':
            turn_right()
            turn_right()

def a_star(dest):
    global DIR
    VISITED = set()
    X = 0
    Y = 0

    pq = PriorityQueue()
    # <dist, <nextx, nexty>>
    #min heap
    pq.put((0, (X, Y)))

    while not pq.empty():
        curr = pq.get()[1]
        print("-----------------------------------")
        print("curr:", X, Y)

        change = sub_pair(curr, (X, Y))

        if change != (0, 0):
            while MOVE[DIR]['f'] != change:
                turn_right()
            move_forward()
            print("move forward to:", curr, "facing:", DIR)

        X = curr[0]
        Y = curr[1]

        if (X, Y) == dest:
            break
        
        dir_order = exploration_order(curr, dest)
        print("dir_order:", dir_order)
        change_dir(DIR, dir_order[0])
        for d in dir_order:
            next_pair = add_pair(curr, MOVE[DIR]['f'])
            if next_pair in VISITED:
                print("DIR:", DIR, "next_pair:", next_pair, "in set")
                turn_right()
                continue

            move_f = can_forward()
            if move_f:
                pq.put((euclidean_dist(next_pair, dest), next_pair)) 
                print("pushing to pq:", next_pair, "dist:", euclidean_dist(next_pair, dest))
                break
            turn_right()
        
        VISITED.add(curr)

    

        
        







if __name__ == "__main__":
    try:
        time.sleep(10)
        a_star((0, 6))
        time.sleep(10)
        a_star((4, 8))
    finally:
        fc.stop()


































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
