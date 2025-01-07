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

def move(dist, speed = 0.5, easein = 100, easeout = 100, startgyro = g.angle):
    startpos = (mr.position + ml.position) / 2
    endpos = startpos + dist
    maxdistance = endpos - startpos
    print(startgyro)
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
        m.on(helper.clamp(move+gyrooffset, -100, 100), helper.clamp(move-gyrooffset, -100, 100))
        # m.on(move, move)
        print(g.angle, startgyro)
    m.off()


def steer(angle, steer, speed = 0.5, chain = False):
    while True:
        if helper.abs(g.angle - angle) < 2 and chain:
            print("bye bye")
            break
        if g.angle - angle == 0:
            print("bye bye 2")
            break
        curspeed = speed*100 if chain else helper.clamp(angle - g.angle, -100, 100) * speed
        print(g.angle, curspeed, chain)
        m.on(curspeed + steer, curspeed- steer)
    m.off(brake=not chain)

steer(20, 5, chain= True)

steer(0, -5, chain= True)

move(200, easein=1, startgyro=0)

sleep(2)

m.off(brake=False)

print("done in", round(run_time(), 1))