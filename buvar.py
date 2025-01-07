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


def steer(angle, steer, speed = 0.5):
    startdist = angle - g.angle
    while True:
        if startdist > 0 and angle < g.angle:
            break
        elif startdist < 0 and angle > g.angle:
            break
        curspeed = speed * helper.clamp(abs(g.angle - angle) * 2, 0, 100)
        if angle < g.angle:
            m.on(curspeed - steer, curspeed + steer)
        elif angle > g.angle:
            m.on(curspeed + steer, curspeed - steer)
        print(g.angle, curspeed)
        if abs(angle - g.angle) < 2:
            break
    m.off()
    print("kész", g.angle)


##futás kód

move(480, startgyro=2)
full_emeles = run_time()
bal_feltet.on_for_rotations(100, 22.5, block=False)
turn(0)
sleep(3)
move(330, speed=0.08, startgyro=1, easeout=1)
full_emeles = run_time() - full_emeles
bal_feltet.on_for_rotations(100, -5)

move(-110)
turn(28)
move(225)
bal_feltet.on_for_rotations(100, -13)
turn(15, easeout=1)

bal_feltet.on_for_rotations(100, 12)
sleep(0.5)
move(135)
turn(-5)
bal_feltet.on_for_rotations(100, 5)
turn(55)
# bal_feltet.on_for_rotations(100, -2, block=False)
sleep(5)
move(670)
turn(35)
move(-30)
bal_feltet.on_for_rotations(100, -5)

turn(50)
move(-100)
turn(15)
bal_feltet.on_for_rotations(100, -12, block=False)
move(200)
sleep(10)


m.off(brake=False)

bal_feltet.off(brake=False)

print("done in", round(run_time(), 1))
print("full emelés", round(full_emeles, 1))
