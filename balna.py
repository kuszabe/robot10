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

starttime = time.time()

def run_time():
    return time.time() - starttime

#implement easing
def turn(degree, speed = 0.8, easein= 60, easeout = 120):
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


def move(dist, speed = 0.7, easein = 100, easeout = 200, startgyro = None, CORRECTION_NODIFIER = 1):
    print("moving")
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
        gyrooffset = (startgyro - g.angle) * CORRECTION_NODIFIER * abs(move / 100)
        m.on(helper.clamp(move+gyrooffset, -100, 100), helper.clamp(move-gyrooffset, -100, 100))
        #írd ki a jelenlegi szögértéket és a startgyro értékét és a gyrooffset értékét
        print(g.angle, startgyro, gyrooffset)
    m.off()



##futás kód
try:
    bal_feltet.off()
    jobb_feltet.off()

    jobb_feltet.on_for_degrees(20, 180, block=False)
    move(700)
    turn(-45)
    move(665)
    turn(44, speed=0.2)
    move(680, startgyro = 45)
    #kiengedi a rákot
    bal_feltet.on_for_degrees(20, -100)
    sleep(1)
    bal_feltet.on_for_degrees(20, 100)

    #visszatolat

    move(-600)
    #párhuzamosan fordul a szonárra
    turn(-60)
    #odamegy a szonár mellé
    jobb_feltet.on_for_degrees(20, 360, block=False)
    move(450)
    #
    jobb_feltet.on_for_degrees(20, 720)
finally:
    m.off(brake=False)

    bal_feltet.off(brake=False)

    print("done in", round(run_time(), 1))
