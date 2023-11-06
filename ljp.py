import vector
import math
from masspoint import MassPoint 
import random

class LJP:
    def __init__(self, particle_mass, particle_amount, eps, ds0, rad, repel_pow = 12, attract_pow = 6, col_lines=[]):
        self.particle_mass   = particle_mass
        self.particle_amount = particle_amount
        self.ds0             = ds0
        self.eps             = eps
        self.repel_pow       = repel_pow
        self.attract_pow     = attract_pow
        self.col_lines       = col_lines
        self.rad             = rad
        self.g               = vector.obj(x = 0., y = 0.)
        self.dt              = 1./30.
        self.damp            = 0.595
        self.particles       = []
        self.min_dist        = 0.00001
        random.seed(1)
        self.init_mps()

    def length(self, vec: vector.VectorObject2D):
        return math.sqrt(vec.x*vec.x + vec.y*vec.y)
    
    def squared_length(self, vec: vector.VectorObject2D):
        return (vec.x*vec.x + vec.y*vec.y)
    
    def init_mps(self):       
        for i in range(0, self.particle_amount):
            for j in range(0, self.particle_amount):
                x = 200 + i * (self.rad + 4.5 ) +  (-.5 + random.random()) 
                y = 200 + j * (self.rad + 4.5 ) +  (-.5 + random.random())
                self.particles.append(MassPoint(.05, vector.obj(x = 0., y = 0.), vector.obj(x = 0., y = 0.), vector.obj(x = x, y = y), 0, self.rad))

    def random_vector(self, range_min, range_max):
        return vector.obj(x=(range_min + ( random.random()*range_max - range_min )), y = (range_min + ( random.random()*range_max - range_min )))
    
    def calc_frame(self):
        for i in range(0, len(self.particles) - 1):
            for j in range(i + 1, len(self.particles)):
                self.force(self.particles[ i ], self.particles[ j ])
        for particle in self.particles:
            for line in self.col_lines:
                self.wall_collide(line[0], line[1], particle)
            particle.vel += self.dt * self.g
            particle.pos += self.dt * particle.vel

        return self.particles
    
    def force(self, A, B):
        sq_dist = self.squared_length(A.pos - B.pos)
        if sq_dist < 100*self.ds0:
            dist = math.sqrt(sq_dist)
            ljp =  self.ljp(dist)
            v_ab = (1/dist)*(A.pos - B.pos)
            v_ba = -v_ab
            accA = ljp/A.mass
            accB = ljp/B.mass
            A.vel += self.dt*accA*v_ab
            B.vel += self.dt*accB*v_ba


    def ljp(self, dist):
        return self.eps*( self.repel_pow*(math.pow(self.ds0, self.repel_pow)/pow(dist, self.repel_pow + 1)) - 2*self.attract_pow*(math.pow(self.ds0, self.attract_pow)/math.pow(dist, self.attract_pow + 1)) )

    def wall_collide(self, wA, wB, P):
        dirLine = wB - wA
        normLine = vector.obj(x = -dirLine.y, y = dirLine.x).unit()

        t = ( P.pos.y*dirLine.x - wA.y*dirLine.x - P.pos.x*dirLine.y + wA.x*dirLine.y ) / ( normLine.x*dirLine.y - normLine.y*dirLine.x )
        
        dist = self.squared_length(t*normLine)

        if dist <= P.rad*P.rad:
            k = -1
            if dirLine.y == 0:
                k = (P.pos.x + t*normLine.x - wA.x)/dirLine.x
            else:
                k = (P.pos.y + t*normLine.y - wA.y)/dirLine.y

            if k >= 0 and k <= 1:
                pHit = wA + k*dirLine
                distVec = pHit - P.pos

                new_v = P.vel +( 2*((-P.vel).dot(normLine)) * normLine )

                diffDist = math.sqrt(dist) - 2*P.rad
                PCorr = distVec.unit() * diffDist 

                P.pos += PCorr
                P.vel = self.damp*new_v