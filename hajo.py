#!/usr/bin/env micropython

from time import sleep
import time
import helper
from ev3dev2.motor import MoveTank, LargeMotor, MediumMotor
from ev3dev2.sensor.lego import GyroSensor

def hajo(m, ml, mr, g, jobb_feltet, bal_feltet):

    def turn(degree, speed = 0.3, easein= 30, easeout = 60):
        print("turning")
        MIN_MOVE = 3
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


    def move(dist, speed = 0.8, easein = 70, easeout = 150, startgyro = None, CORRECTION_NODIFIER = 0.5):
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
            #írd ki a jelenlegi szögértéket és a startgyro értékét és a gyrooffset értékét
            print(g.angle, startgyro, gyrooffset)
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

    ##futás kód
    move(1000) #előremegy a hajó mellé
    move(800, CORRECTION_NODIFIER=3, startgyro=0) #itt továbbmegy és már viszi magával a hajót, ezért nagyobb a korrekciós szorzó, így egyenes tud maradni a hajó plusz súlyával is

    #ezek a mozgások a közvetlenül a hajó mellé igazítják a robotot
    move(-150)
    turn(25)
    move(300)
    turn(0)

    bal_feltet.on_for_degrees(10, 90) #lerakja a kart a mesterséges élőhelyre
    bal_feltet.on_for_seconds(10, 3, block=False) #lenyomva tarja három másodpercig
    move(-200, startgyro=0, speed=0.08) # lassan hátramegy és felállítja a mesterséges élőhelyet

    
    move(-600, speed=0.9) #visszatolat
    bal_feltet.on_for_degrees(100, -200) #felemeli a kart, hogy ne legyen útban
    turn(25) # srégen a fel felé fordul
    move(1200, CORRECTION_NODIFIER=0) # kikapcsolt gyrokorrekcióval előre megy így a falhoz igazítja magát és ezzel tolja be a hajót a helyére
    move(-100) #hátratolat egy kicsit, hogy ne érjen hozzá a hajóhoz


if __name__ == "__main__":
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

    try:
        hajo(m, ml, mr, g, jobb_feltet, bal_feltet)
    finally:
        m.off(brake=False)
        bal_feltet.off(brake=False)
        jobb_feltet.off(brake=False)
        print("done in", round(run_time(), 1))