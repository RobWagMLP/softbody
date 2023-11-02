import vector

class MassPoint:
    mass: 5
    vel: vector.obj(x = 0., y = 0.)
    acc: vector.obj(x = 0., y = 0.)
    pos: vector.obj(x = 0., y = 0.)
    rad: 300

    g:  vector.obj(x = 0., y = 0.)

    def __init__(self, imass, ivel, iacc, ipos, id, rad=10):
        self.mass = imass
        self.vel  = ivel
        self.acc  = iacc
        self.pos  = ipos
        self.id   = id
        self. rad = rad