#!/usr/bin/env micropython

from time import sleep
import time

starttime = time.time()

def run_time():
    return time.time() - starttime

import math

import helper

from ev3dev2.motor import MoveTank, LargeMotor, MediumMotor
from ev3dev2.sensor.lego import GyroSensor

m = MoveTank("D", "A")
ml = LargeMotor("D")
mr = LargeMotor("A")
g = GyroSensor("in2")
jobb_feltet = MediumMotor("B")



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

def move(dist, speed = 0.5, easein = 100, easeout = 150):
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
        m.on(helper.clamp(move+gyrooffset, -100, 100), helper.clamp(move-gyrooffset, -100, 100))
        # m.on(move, move)
        print(g.angle, startgyro)
    m.off()



move(300)
turn(30)
move(420)
turn(-15)
move(350)
turn(34)
move(500)
turn(85)
move(970)
turn(0)


move(130)


jobb_feltet.on_for_degrees(5, -250)

turn(90)

move(850)
move(780)
turn(180)
move(1200)
turn(130)
move(-200)
move(600)

# sleep(2)

# turn(95)

# move_with_ease(1500, easeout=300)



m.off(brake=False)
jobb_feltet.off(brake=False)
print(run_time())