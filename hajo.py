#!/usr/bin/env micropython

from time import sleep
import time

starttime = time.time()

def run_time():
    return time.time() - starttime

import helper

from ev3dev2.motor import MoveTank, LargeMotor, MediumMotor
from ev3dev2.sensor.lego import GyroSensor

m = MoveTank("D", "A")
ml = LargeMotor("D")
mr = LargeMotor("A")
g = GyroSensor("in2")
bal_feltet = MediumMotor("C")
jobb_feltet = MediumMotor("B")

g.calibrate()


#fancy move function
def turn(degree, speed = 0.8, easein= 60, easeout = 120):
    MIN_MOVE = 7
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
    m.off()

def move(dist, speed = 0.7, easein = 100, easeout = 200, startgyro = None, CORRECTION_NODIFIER = 0.5):
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
        gyrooffset = (startgyro - g.angle) * CORRECTION_NODIFIER * move / 100
        m.on(helper.clamp(move+gyrooffset, -100, 100), helper.clamp(move-gyrooffset, -100, 100))
        #írd ki a jelenlegi szögértéket és a startgyro értékét
        print(g.angle, startgyro)
    m.off()

def move_with_turn_offset(dist, speed = 0.8, easein = 100, easeout = 200, startgyro = None, CORRECTION_MODIFIER = 3, turn_offset = 0):
    MIN_MOVE = 5
    if startgyro == None:
        startgyro = g.angle
    startpos = (mr.position + ml.position) / 2
    endpos = startpos + dist
    maxdistance = endpos - startpos
    print(startgyro)
    while True:
        currentpos = (mr.position + ml.position) / 2
        distance = endpos - currentpos
        gyrooffset = (startgyro - g.angle) * CORRECTION_MODIFIER
        if helper.abs(distance) < 3:
            break
        if helper.abs(distance) < easeout:
            sign = distance/helper.abs(distance)
            move = helper.clamp(helper.abs(distance) * speed * (100/easeout), MIN_MOVE, 100) * sign
            gyrooffset = startgyro - g.angle
            print("easeout")
        elif helper.abs(distance) > helper.abs(maxdistance) - easein:
            move = helper.clamp((helper.abs(maxdistance) - helper.abs(distance)), -100, 100)
            sign = distance / helper.abs(distance)
            move = helper.clamp((move * speed * (100/easein) + 5) * sign, -100, 100)
        else:
            sign = distance / helper.abs(distance)
            move = helper.clamp(speed * 100 * sign, -100, 100)
        m.on(helper.clamp(move+gyrooffset-turn_offset, -100, 100), helper.clamp(move-gyrooffset + turn_offset, -100, 100))
        # m.on(move, move)
        print(g.angle, startgyro)
    m.off()

print("started at", round(run_time(), 1))

try:
    ##futás kód
    move(1200)
    turn(2)
    move(770, startgyro=3, CORRECTION_NODIFIER=3)
    turn(2)
    bal_feltet.on_for_degrees(10, 90)
    bal_feltet.on_for_seconds(10, 1)
    move(-150, startgyro=0, speed=0.1)
    move(-600)
    bal_feltet.on_to_position(100, 0, block=False)
    turn(30)
    move(800, CORRECTION_NODIFIER=0)
    turn(0)
    move(400)
    move(-100)
    sleep(1)

finally:
    m.off(brake=False)
    bal_feltet.off(brake=False)
    jobb_feltet.off(brake=False)
    print("done in", round(run_time(), 1))