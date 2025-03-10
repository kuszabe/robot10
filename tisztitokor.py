#!/usr/bin/env micropython

from time import sleep
import time

import math

import helper

from ev3dev2.motor import MoveTank, LargeMotor, MediumMotor
from ev3dev2.sensor.lego import GyroSensor

m = MoveTank("D", "A")
ml = LargeMotor("D")
mr = LargeMotor("A")
g = GyroSensor("in2")
jobb_feltet = MediumMotor("B")
bal_feltet = MediumMotor("C")

# bal_feltet.on_for_rotations(20, -1, block=False)

g.reset()
g.calibrate()

starttime = time.time()

def run_time():
    return time.time() - starttime

#fancy move function
def turn(degree, speed = 0.5, easein= 30, easeout = 60):
    MIN_MOVE = 3
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
        print("elcseszte", g.angle, degree)
    m.off()


def move(dist, speed = 0.7, easein = 100, easeout = 200, startgyro = None, CORRECTION_NODIFIER = 3):
    MIN_MOVE = 5
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
        if helper.abs(distance) < 2:
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
        #írd ki a jelenlegi szögértéket és a startgyro értékét és a gyrooffset értékét
        print(g.angle, startgyro, gyrooffset)
        m.on(helper.clamp(move+gyrooffset, -100, 100), helper.clamp(move-gyrooffset, -100, 100))
    m.off()
    if startgyro != g.angle:
        print("a menés végén rossz volt az angle", g.angle)
try:
    bal_feltet.on_for_rotations(30, 2.1, block=False)
    move(280)
    turn(20)
    move(400, startgyro=20)
    turn(-5)
    move(300, startgyro=-5)

    #collects the two
    turn(37)
    move(530, startgyro=37)

    turn(80)

    move(920, startgyro=80)

    bal_feltet.on_for_rotations(30, -0.9, block=False)
    

    #itt fordul rá a karikára
    turn(0, speed=0.4)

    move(140, speed=0.4)

    #actual lifting
    jobb_feltet.on_for_degrees(20, -250, block=False)

    bal_feltet.on_for_rotations(20, 1.5)

    

    input()

    
    #elkezd átmenni a pálya másik oldalára
    bal_feltet.on_for_rotations(100, -2.1, block=False)

    turn(95, speed=0.3)


    move(1200)

    turn(77)

    move(530)

    turn(180)

    move(1000)


    turn(90+45)
    move(-500)
    move(1000)

    
finally:
    m.off(brake=False)
    jobb_feltet.off(brake=False)
    bal_feltet.off(brake=False)
    print("\n", run_time())