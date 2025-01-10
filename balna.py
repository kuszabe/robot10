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



g.reset()
g.calibrate()

#fancy move function
#implement easing
def turn(degree, speed = 0.5, easein= 60, easeout = 120):
    MIN_MOVE = 5
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

def move(dist, speed = 0.5, easein = 100, easeout = 200, startgyro = None):
    MIN_MOVE = 2
    if startgyro == None:
        startgyro = g.angle
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
            sign = distance/helper.abs(distance)
            move = helper.clamp(helper.abs(distance) * speed * (100/easeout), MIN_MOVE, 100) * sign
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



##futás kód
bal_feltet.off()
jobb_feltet.off()

move(700)
turn(-45)
move(665)
turn(45)
move(680, startgyro = 45)
#kiengedi a rákot
bal_feltet.on_for_degrees(20, -100)
sleep(1)
bal_feltet.on_for_degrees(20, 100)

#visszatolat

#párhuzamosan fordul a szonárra

#odamegy a szonár mellé

#

m.off(brake=False)

bal_feltet.off(brake=False)

print("done in", round(run_time(), 1))
