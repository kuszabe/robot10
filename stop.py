from ev3dev2.motor import MoveTank, MediumMotor

m = MoveTank("D", "A")
jobb_feltet = MediumMotor("B")


m.off(brake=False)
jobb_feltet.off(brake=False)
