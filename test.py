#!/usr/bin/env micropython

from time import sleep
import time

starttime = time.time()

def run_time():
    return time.time() - starttime

import math

import helper

from ev3dev2.motor import MoveTank, LargeMotor
from ev3dev2.sensor.lego import GyroSensor

m = MoveTank("D", "A")
ml = LargeMotor("D")
mr = LargeMotor("A")
g = GyroSensor("in2")



g.reset()
g.calibrate()

#fancy move function
#implement easing
def turn(degree, speed = 0.5, easein= 60, easeout = 120):
    maxdistance = degree - g.angle
    while True:
        distance = degree - g.angle
        if distance == 0:
            break
        if helper.abs(distance) < easeout:
            move = distance * speed * (100/easeout)
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

def move(dist, speed = 0.5, easein = 100, easeout = 200):
    startpos = (mr.position + ml.position) / 2
    endpos = startpos + dist
    maxdistance = endpos - startpos
    startgyro = g.angle
    while True:
        currentpos = (mr.position + ml.position) / 2
        distance = endpos - currentpos
        if helper.abs(distance) < 3:
            break
        if helper.abs(distance) < easeout:
            move = distance * speed * (100/easeout)
        elif helper.abs(distance) > helper.abs(maxdistance) - easein:
            move = helper.clamp((helper.abs(maxdistance) - helper.abs(distance)), -100, 100)
            sign = distance / helper.abs(distance)
            move = helper.clamp((move * speed * (100/easein) + 5) * sign, -100, 100)
        else:
            sign = distance / helper.abs(distance)
            move = helper.clamp(speed * 100 * sign, -100, 100)
        gyrooffset = startgyro - g.angle
        m.on(move+gyrooffset/2, move-gyrooffset/2)
            
        print(g.angle, startgyro)
    m.off()


move(600)
turn(90)
move(300)
turn(0)
move(200, speed=0.3, easeout=100)
turn(-90)
move(300)
turn(0)
move(-800)


m.off(brake=False)

print(run_time())