from ev3dev2.motor import MoveTank, MediumMotor

m = MoveTank("D", "A")
jobb_feltet = MediumMotor("B")
bal_feltet = MediumMotor("C")


m.off(brake=False)
jobb_feltet.off(brake=False)
bal_feltet.off(brake=False)
