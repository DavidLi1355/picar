import picar_4wd as fc
import random
import time
import numpy as np
import matplotlib.pyplot as plt

speed = 20


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
    time.sleep(0.3)

    dist_list = []
    while True:
        dist = fc.get_distance_at(current_angle)
        dist_list.append(dist)
        if current_angle == 90:
            break
        current_angle += 10
    
    return dist_list



def main():
    while True:
        scan_list = fc.scan_step(35)
        print(scan_list)
"""
        if not scan_list:
            continue
        
        print(scan_list)
        tmp = scan_list[3:7]
        print(tmp)
        
        if tmp != [2,2,2,2]:
            moveBack()
            turnPatter(x, y)
    plt.show()ra = random.randint(-3, 1)
            if turnPara == 0:
                turnPara = 1
            turn(turnPara/5)
        else:
            fc.forward(speed)
"""

def get_xy_coord(dist, angle):
    x = np.cos(angle * np.pi / 180) * dist
    y = np.sin(angle * np.pi / 180) * dist
    return x, y


if __name__ == "__main__":
    dist_list = np.array(scan_environment())
    angle_list = np.array([i for i in range(0, 190, 10)])
    x, y = get_xy_coord(dist_list, angle_list)
    print(dist_list)
    print(angle_list)
    plt.scatter(x, y)
    plt.show()
    # try: 
    #     main()
    # finally: 
    #     fc.stop()
        

        
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
