#!/usr/bin/env micropython

from time import sleep
import time

import helper

from ev3dev2.motor import MoveTank, LargeMotor, MediumMotor
from ev3dev2.sensor.lego import GyroSensor

m = MoveTank("D", "A")
ml = LargeMotor("D")
mr = LargeMotor("A")
g = GyroSensor("in2")
jobb_feltet = MediumMotor("B")
bal_feltet = MediumMotor("C")


g.reset()
g.calibrate()

starttime = time.time()

def run_time():
    return time.time() - starttime

def turn(degree, speed = 0.3, easein= 30, easeout = 60):
    print("turning")
    MIN_MOVE = 2
    maxdistance = degree - g.angle
    while True:
        distance = degree - g.angle
        if distance == 0:
            break
        if helper.abs(distance) < easeout:
            sign = distance/helper.abs(distance)
            move = helper.clamp(helper.abs(distance) * speed * (100/easeout), MIN_MOVE, 100) * sign
        elif helper.abs(distance) > helper.abs(maxdistance) - easein:
            move = helper.clamp((helper.abs(maxdistance) - helper.abs(distance)), -100, 100)
            sign = distance / helper.abs(distance)
            move = helper.clamp((move * speed * (100/easein) + 5) * sign, -100, 100)
        else:
            sign = distance / helper.abs(distance)
            move = helper.clamp(100 * sign, -100, 100) * speed
        m.on(move, -move)
        # print(g.angle, distance, move)
    if degree != g.angle:
        print("elcseszte", g.angle)
        if abs(degree - g.angle) > 5:
            turn(degree)
    m.off()
    print(g.angle)


def move(dist, speed = 0.7, easein = 70, easeout = 150, startgyro = None, CORRECTION_NODIFIER = 0.5):
    print("moving")
    MIN_MOVE = 2
    if startgyro == None:
        startgyro = g.angle
    startpos = (mr.position + ml.position) / 2
    endpos = startpos + dist
    maxdistance = endpos - startpos
    #írd ki a startgyro értékét
    print(startgyro)
    while True:
        currentpos = (mr.position + ml.position) / 2
        distance = endpos - currentpos
        if helper.abs(distance) < 3:
            break
        if helper.abs(distance) < easeout:
            sign = distance/helper.abs(distance)
            move = helper.clamp(helper.abs(distance) * speed * (100/easeout), MIN_MOVE, 100) * sign
        elif helper.abs(distance) > helper.abs(maxdistance) - easein:
            move = helper.clamp((helper.abs(maxdistance) - helper.abs(distance)), -100, 100)
            sign = distance / helper.abs(distance)
            move = helper.clamp((move * speed * (100/easein) + 5) * sign, -100, 100)
        else:
            sign = distance / helper.abs(distance)
            move = helper.clamp(speed * 100 * sign, -100, 100)
        gyrooffset = (startgyro - g.angle) * CORRECTION_NODIFIER * abs(move / 100)
        m.on(helper.clamp(move+gyrooffset, -100, 100), helper.clamp(move-gyrooffset, -100, 100))
        #írd ki a jelenlegi szögértéket és a startgyro értékét és a gyrooffset értékét
        print(g.angle, startgyro, gyrooffset)
    m.off()



try:
    move(490, speed=0.5)
    bal_feltet.on_for_rotations(60, -4.7, block=False)
    move(330, speed=0.245, startgyro=0)
    bal_feltet.on_for_rotations(100, 1.2)

    sleep(0.2)

    move(-110, speed=0.5)
    turn(28)
    move(270)
    bal_feltet.on_for_rotations(100, 2.7)
    turn(15, easeout=1)

    bal_feltet.on_for_rotations(100, -2.5)
    move(130)
    turn(-8)
    bal_feltet.on_for_rotations(100, -1.7)
    turn(52, speed=0.5)
    bal_feltet.on_for_rotations(100, 1.7, block=False)
    move(375)
    turn(0, speed=0.5)
    move(450)
    turn(90, speed=0.5)
    bal_feltet.on_for_rotations(100, -1)
    turn(80)
    bal_feltet.on_for_rotations(100, 1)
    turn(90)

    bal_feltet.on_for_rotations(100,-1.5)
    turn(50)
    move(50)
    bal_feltet.on_for_rotations(100, 4)

    bal_feltet.on_for_rotations(100, -2.5)
    turn(-80)
    bal_feltet.on_for_rotations(100, 3)

    bal_feltet.on_for_rotations(100, -4, block=False)
    sleep(0.5)
    turn(10)
    move(-2000, speed=1)

    # move(490, speed=0.5, CORRECTION_NODIFIER=1)
    # bal_feltet.on_for_rotations(100, -4.9, block=False)
    # move(310, speed=0.24, startgyro=0, CORRECTION_NODIFIER=3)
    # bal_feltet.on_for_rotations(100, 1.2)

    # move(-390)
    # turn(33)
    # bal_feltet.on_for_rotations(100, 1.1, block=False)
    # move(1210)
    # turn(-90, speed=0.2)
    # bal_feltet.on_for_rotations(100, -1)
    # move(235, speed=0.2, CORRECTION_NODIFIER=3, startgyro=-90)
    # bal_feltet.on_for_rotations(100, -1.2)
    # move(100)
    # move(-100)
    # turn(-30)
    # move(-390)
    # bal_feltet.on_for_rotations(100, 0.9, block=False)
    # turn(26, speed=0.2)
    # move(330)
    # bal_feltet.on_for_rotations(100, 0.7)
    # move(-200)
    # turn(-50)
    # move(300)
    # bal_feltet.on_for_rotations(100, 3)
    # sleep(0.5)
    # bal_feltet.on_for_rotations(100, -3)
    # turn(40)
    # sleep(1)


finally:
    m.off(brake=False)
    bal_feltet.off(brake=False)
    jobb_feltet.off(brake=False)
    print("done in", round(run_time()))