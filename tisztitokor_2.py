#!/usr/bin/env micropython
import helper
from time import sleep
from ev3dev2.motor import MoveTank, LargeMotor, MediumMotor
from ev3dev2.sensor.lego import GyroSensor
import time

def tisztitokor(m, ml, mr, g: helper.GyroWrapper, jobb_feltet: MediumMotor, bal_feltet):

    def turn(degree, speed = 0.4, easein= 30, easeout = 70, timeout = 0):
        starttime = time.time()
        print("turning")
        MIN_MOVE = 2
        maxdistance = degree - g.angle
        while True:
            if timeout != 0 and ((time.time() - starttime) > timeout):
                print("timeout-olt")
                break
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
        if degree != g.angle and not timeout:
            print("elcseszte", g.angle, degree)
            if abs(degree - g.angle) > 2:
                turn(degree)
        m.off()
        print(g.angle)


    def move(dist, speed = 0.8, easein = 70, easeout = 150, startgyro = None, CORRECTION_NODIFIER = 1):
        print("moving")
        MIN_MOVE = 3
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
        m.off()


    move(200)
    turn(25)
    move(800, startgyro=25)
    move(-200, startgyro=25)
    turn(-15)
    move(400, startgyro=-15)
    move(-500, startgyro=-15)
    turn(0)
    move(800, startgyro=0)
    turn(-87)
    jobb_feltet.on_for_rotations(10, 0.2, block=False)
    move(-1060, startgyro=-87)
    turn(0)
    sleep(0.2)
    move(110, speed=0.4, CORRECTION_NODIFIER=3)
    #felemeli a targoncát
    jobb_feltet.on_for_rotations(70, 3.3)
    turn(60)
    jobb_feltet.on_for_rotations(100, -2.9, block=False)
    move(100, startgyro=60, speed=0.5)
    turn(38, timeout=2)
    jobb_feltet.on_for_rotations(70, 2)
    move(-50)

    turn(190, speed=0.25, timeout=2)

    jobb_feltet.on_for_rotations(70, 1, block=False)

    turn(97)
    move(1150)

    turn(80)
    move(500)
    move(-200)
    turn(180)
    move(1050)
    turn(135)
    move(-420, speed=1)
    move(1000, speed=1)

if __name__ == "__main__":
    m = MoveTank("D", "A")
    ml = LargeMotor("D")
    mr = LargeMotor("A")
    g = GyroSensor("in2")
    jobb_feltet = MediumMotor("B")
    bal_feltet = MediumMotor("C")

    g.reset()
    g.calibrate()

    try:
        helper.startbench("futas")
        tisztitokor(m, ml, mr, g, jobb_feltet, bal_feltet)
    finally:
        helper.endbench("futas")
        m.off(brake=False)
        jobb_feltet.off(brake=False)