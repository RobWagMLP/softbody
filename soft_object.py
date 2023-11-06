
import vector
import math
from masspoint import MassPoint 

class SoftObject:  

    def __init__(self, grid, iD = 10, is0=100, iRadMass = 30, iMass = 5, lines=[]):
        self.D   = iD
        self.s0  = is0
        self.s0D = math.sqrt(2*(is0*is0))
        self.radMass = iRadMass
        self.mass = iMass
        self.masspoints = []
        self.collisionDamp = .85
        self.dt = 1/100.
        self.damping = .995
        self.init_mp(grid)
        self.g = vector.obj(x = 0., y = 1100)
        self.deltaThreshold = 0.001
        self.lines = lines

    def length(self, vec: vector.VectorObject2D):
        return math.sqrt(vec.x*vec.x + vec.y*vec.y)
    
    def init_mp(self, grid):
        for i in range(0, len(grid)):
            self.masspoints.append([])
            for j in range(0, len(grid[i])):
                self.masspoints[i].append({"mp": MassPoint(self.radMass, vector.obj(x = 0, y = 0), vector.obj(x = 0, y = 0), vector.obj(x = grid[i][j]["point"].x, y = grid[i][j]["point"].y), grid[i][j]["pId"], self.radMass), "collision": {"i": -1, "j": -1, "dist": 99999999}})

    
    def update_stats(self):
        for i in range(0, len(self.masspoints )):
            row = self.masspoints[i]
            for j in range(0, len(row)):
                point = row[j]
                if i > 0:
                    ref_point = self.masspoints[i - 1][j]
                    self.calc_vel(point["mp"], ref_point["mp"], self.s0)
                if i > 0 and j < len(row) -1:
                    ref_point = self.masspoints[i - 1][j + 1]
                    self.calc_vel(point["mp"], ref_point["mp"], self.s0D)
                if j < len(row) -1:
                    ref_point = self.masspoints[i][j + 1]
                    self.calc_vel(point["mp"], ref_point["mp"], self.s0)
                if j < len(row) -1 and i < len(self.masspoints) - 1:
                    ref_point = self.masspoints[i + 1][j + 1]
                    self.calc_vel(point["mp"], ref_point["mp"], self.s0D)

        self.self_collision(point)
        return self.masspoints


    def calc_vel(self, A: vector.VectorObject2D, B: vector.VectorObject2D, s0):
        
        dist: vector.VectorObject2D = (B.pos - A.pos)
        norm = dist.unit()

        hA = norm*s0
        hB = -hA

        D = vector.obj(x = self.D, y = self.D)

        dSA = ((B.pos - A.pos) - hA)
        dSB = ((A.pos - B.pos) - hB)
        
        if self.length(dSA) < self.deltaThreshold:
            return
        
        A.acc  = vector.obj(x = ((D.x * dSA.x)/A.mass), y = ((D.y * dSA.y)/A.mass ))
        B.acc  = vector.obj(x = ((D.x * dSB.x)/B.mass), y = ((D.y * dSB.y)/B.mass ))
        
        A.vel += self.dt * A.acc
        B.vel += self.dt * B.acc

        A.vel *= self.damping
        B.vel *= self.damping

    def self_collision(self, MP):
        rads = 2*self.radMass
        for i in range(0, len(self.masspoints)):
            for j in range(0, len(self.masspoints[i])):
                self.check_distance(i, j, self.masspoints[i][j])

        for i in range(0, len(self.masspoints)):
            for j in range(0, len(self.masspoints[i])):
                val = self.masspoints[i][j]
                if val["collision"]["dist"] < rads:
                     
                    k = val["collision"]["i"]
                    l = val["collision"]["j"]

                    if k < i or (k == i and l < j):
                        continue         

                    self.reflect(val["mp"], self.masspoints[k][l]["mp"], val["collision"]["dist"] - rads)
                    self.masspoints[k][l]["mp"].vel *= self.collisionDamp
                    val["collision"]["dist"]      = 999999
                    self.masspoints[k][l]["collision"]["dist"] = 999999

                ddt = self.dt*0.5
                for u in range (0, 2):
                    val["mp"].vel += ddt * self.g
                    val["mp"].pos += ddt * val["mp"].vel
                    for line in self.lines:
                        self.collide_mp_with_line(line[0], line[1], val["mp"])
    
    def check_distance(self,i, j, A):
        for k in range(i, len(self.masspoints)):
            a = 0
            if k == i:
                a = j +1
            for l in range(a, len(self.masspoints[k])):
                val = self.masspoints[k][l]
                dist = self.length(A["mp"].pos - val["mp"].pos)
                if dist < A["collision"]["dist"]:
                    A["collision"]["dist"] = dist
                    A["collision"]["i"]    = k
                    A["collision"]["j"]    = l
                if dist < val["collision"]["dist"]:
                    val["collision"]["dist"] = dist
                    val["collision"]["i"]    = i
                    val["collision"]["j"]    = j

    def reflect(self,A, B, diff):
        vel_a : vector.VectorObject2D = A.vel
        vel_b : vector.VectorObject2D = B.vel
 
        v_abs_a = self.length(vel_a)
        v_abs_b = self.length(vel_b)

        dist  = B.pos - A.pos
        #norm  = vector.obj(x= - dist.y, y = dist.x)
        normBA  = dist.unit()
        normAB  = - normBA

        vel_new_a = vel_a + (math.fabs( 2*((-vel_a).dot(normAB))) * normAB )
        vel_new_b = vel_b + (math.fabs( 2*((-vel_b).dot(normBA))) * normBA )

        hp = 2*((A.mass * v_abs_a + B.mass * v_abs_b)/(A.mass + B.mass))
        
        #A.vel = 10.36*vel_new_a.unit()
        #B.vel = 197.84*vel_new_b.unit()

        gA = (hp - v_abs_a)
        gB = (hp - v_abs_b)
        A.vel = gA * ( vel_new_a.unit() )
        B.vel = gB * ( vel_new_b.unit() )

        print(2*((-vel_a).dot(normAB)),  2*((-vel_b).dot(normBA)))

        print("\n")
        
        Acorr = dist.unit() * (.51*diff)       
        A.pos += Acorr

        Bcorr = (-dist).unit() * (.51*diff)       
        B.pos += Bcorr
             
    def collide_all_with_line(self, aL: vector.VectorObject2D, bL: vector.VectorObject2D):
        for row in self.masspoints:
            for mp in row:
                self.collide_mp_with_line(aL, bL, mp["mp"])

    def collide_mp_with_line(self, aL: vector.VectorObject2D, bL: vector.VectorObject2D, P: MassPoint):
        dirLine = bL - aL
        normLine = vector.obj(x = -dirLine.y, y = dirLine.x).unit()

        t = ( P.pos.y*dirLine.x - aL.y*dirLine.x - P.pos.x*dirLine.y + aL.x*dirLine.y ) / ( normLine.x*dirLine.y - normLine.y*dirLine.x )
        dist = self.length(t*normLine)

        if dist <= P.rad:
            k = -1
            if dirLine.y == 0:
                k = (P.pos.x + t*normLine.x - aL.x)/dirLine.x
            else:
                k = (P.pos.y + t*normLine.y - aL.y)/dirLine.y

            if k >= 0 and k <= 1:
                pHit = aL + k*dirLine
                distVec = pHit - P.pos

                new_v = P.vel +( 2*((-P.vel).dot(normLine)) * normLine )

                diffDist = dist - 2*P.rad
                PCorr = distVec.unit() * diffDist 

                P.pos += PCorr
                P.vel = self.collisionDamp*new_v
       