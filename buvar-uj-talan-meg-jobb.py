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

#implement easing
def turn(degree, speed = 0.4, easein= 30, easeout = 80):
    print("turning")
    MIN_MOVE = 1
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


def move(dist, speed = 0.7, easein = 70, easeout = 200, startgyro = None, CORRECTION_NODIFIER = 1):
    print("moving")
    MIN_MOVE = 3
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

starttime = time.time()

def run_time():
    return time.time() - starttime

try:
    move(440, speed=0.6)
    turn(-1)
    bal_feltet.on_for_rotations(50, -4.8, block=False)
    sleep(0.5)
    move(320, speed=0.30, startgyro=-1)
    bal_feltet.on_for_rotations(100,1)

    move(-200, speed=0.4)
    turn(45)
    move(1000)
    turn(-50)
    bal_feltet.on_for_rotations(60, 3.8, block=False)
    move(220)
    sleep(0.5)
    bal_feltet.on_for_rotations(100, -3.1)

    turn(-87)
    move(60, speed=0.5, CORRECTION_NODIFIER=3)
    bal_feltet.on_for_rotations(100, -1.5)
    move(140)

    move(-40, startgyro=-87)
    turn(-45)
    move(-200, speed=0.4)
    turn(42, speed=0.3)
    bal_feltet.on_for_rotations(100, 0.5)
    move(200)
    bal_feltet.on_for_rotations(100, 0.5)
    turn(35)
    move(-20)
    bal_feltet.on_for_rotations(100, 0.5)
    move(-200)
    turn(32)
    move(260)
    bal_feltet.on_for_rotations(100, 2)
    bal_feltet.on_for_rotations(100, -2)
    move(-600)
    turn(0)
    move(-1000)


    sleep(3)

finally:

    print(g.angle)

    m.off(brake=False)
    bal_feltet.off(brake=False)

    print("done in", round(run_time()))