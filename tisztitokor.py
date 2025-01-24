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
def turn(degree, speed = 0.7, easein= 60, easeout = 120):
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
    m.off()

def move(dist, speed = 0.7, easein = 100, easeout = 200, startgyro = None):
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


def move_steer(dist, angle, maxturn = 10, speed = 0.5, easein = 100, easeout = 100, turn_offset = 0):
    startpos = (mr.position + ml.position) / 2
    endpos = startpos + dist
    maxdistance = endpos - startpos
    startgyro = g.angle
    print(angle)
    while True:
        currentpos = (mr.position + ml.position) / 2
        distance = endpos - currentpos
        steer = helper.clamp(angle - g.angle, -maxturn, maxturn)
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
        if helper.abs(distance) > helper.abs(maxdistance) - turn_offset:
            print("still not turning", g.angle)
            steer = startgyro - g.angle
        m.on(helper.clamp(move+steer, -100, 100), helper.clamp(move-steer, -100, 100))
    m.off()

move(300)
turn(20)
move(370)
turn(-12)
move(350)

#collects the two
turn(39)
move(500)

#to the part where it uses the lift
# turn(65)
# move(260)
# turn(90)
# move(760)

turn(60)
move_steer(1000, 90, turn_offset=100)

turn(0, speed=0.4)


move(100, speed=0.3)

#actual lifting
jobb_feltet.on_for_degrees(20, -250)


sleep(0.5)

turn(95, speed=0.3)

# sleep(10)

move_steer(1700, 75, speed=0.8, easeout=300, turn_offset=900)

turn(180, speed=0.3)

move(1100, speed=0.8)

turn(135)

move(-500, speed=0.8)

sleep(0.5)

move(1000, speed=0.9)

m.off(brake=False)
jobb_feltet.off(brake=False)
print(run_time())