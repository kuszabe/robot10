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


def move(dist, speed = 0.7, easein = 70, easeout = 200, startgyro = None, CORRECTION_NODIFIER = 0.5):
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
    move(200)
    turn(25)
    move(600, startgyro=25)
    turn(-12)
    move(400, startgyro=-15)
    move(-500, startgyro=-15)
    turn(0)
    move(650, startgyro=0)
    turn(85)
    move(1020)
    turn(0)
    move(130, speed=0.3, CORRECTION_NODIFIER=3)
    #felemeli a targoncát
    jobb_feltet.on_for_rotations(70, 3.5)
    turn(60)
    move(100, startgyro=60, speed=0.5)
    jobb_feltet.on_for_rotations(70, -3)
    turn(40)
    jobb_feltet.on_for_rotations(70, 2)
    sleep(0.5)

    move(-100, startgyro=38)

    jobb_feltet.on_for_rotations(100, 1, block=False)

    turn(190)

    move(-100, startgyro=190)

    turn(100)
    move(1150)

    turn(75)
    move(500)
    turn(190)
    move(1100)
    turn(135)
    move(-370, speed=1)
    move(800)
    # move

finally:

    m.off(brake=False)
    jobb_feltet.off(brake=False)

    print("done in", round(run_time()))