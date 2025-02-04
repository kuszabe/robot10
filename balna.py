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
bal_feltet = MediumMotor("C")
jobb_feltet = MediumMotor("B")

g.calibrate()

starttime = time.time()

def run_time():
    return time.time() - starttime

def turn(degree, speed = 0.3, easein= 30, easeout = 60):
    print("turning")
    MIN_MOVE = 2
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


def move(dist, speed = 0.7, easein = 70, easeout = 150, startgyro = None, CORRECTION_NODIFIER = 0.5):
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

    move(850)
    turn(-45)
    move(480)
    turn(45)
    move(605, startgyro=45)
    jobb_feltet.on_for_degrees(10, 160)
    sleep(1)
    jobb_feltet.on_for_degrees(-10, 160)
    move(-460)
    bal_feltet.on_for_degrees(-20, 90)

    turn(0)
    move(500)
    bal_feltet.on_for_degrees(-20, 1800)

finally:
    m.off(brake=False)

    bal_feltet.off(brake=False)

    print("done in", round(run_time(), 1))
