
import vector
import math
from masspoint import MassPoint 

class SoftObject:  

    def __init__(self, grid, iD = 10, is0=100, iRadMass = 30, iMass = 5):
        self.D   = iD
        self.s0  = is0
        self.s0D = math.sqrt(2*(is0*is0))
        self.radMass = iRadMass
        self.mass = iMass
        self.masspoints = []
        self.collisionDamp = .9
        self.dt = 1/60.
        self.damping = .999
        self.init_mp(grid)
        self.g = vector.obj(x = 0., y = 98.1)

    def length(self, vec: vector.VectorObject2D):
        return math.sqrt(vec.x*vec.x + vec.y*vec.y)
    
    def init_mp(self, grid):
        for i in range(0, len(grid)):
            self.masspoints.append([])
            for j in range(0, len(grid[i])):
                self.masspoints[i].append({"mp": MassPoint(self.radMass, vector.obj(x = 0, y = 0), vector.obj(x = 0, y = 0), vector.obj(x = grid[i][j]["point"].x, y = grid[i][j]["point"].y), grid[i][j]["pId"], self.radMass), "surr": {"up": -1, "ro": -1, "rr": -1, "ru": -1, "du": -1, "lu": -1, "ll": -1, "lo": -1}})

    
    def update_stats(self):
        for i in range(0, len(self.masspoints )):
            row = self.masspoints[i]
            for j in range(0, len(row)):
                point = row[j]
                if i > 0:
                    ref_point = self.masspoints[i - 1][j]
                    l = self.calc_vel(point["mp"], ref_point["mp"], self.s0)
                    point["surr"]["up"] = l
                    ref_point["surr"]["du"] = -l
                if i > 0 and j < len(row) -1:
                    ref_point = self.masspoints[i - 1][j + 1]
                    l = self.calc_vel(point["mp"], ref_point["mp"], self.s0D)
                    point["surr"]["ro"] = l
                    ref_point["surr"]["lu"] = -l
                if j < len(row) -1:
                    ref_point = self.masspoints[i][j + 1]
                    l = self.calc_vel(point["mp"], ref_point["mp"], self.s0)
                    point["surr"]["rr"] = l
                    ref_point["surr"]["ll"] = -l
                if j < len(row) -1 and i < len(self.masspoints) - 1:
                    ref_point = self.masspoints[i + 1][j + 1]
                    l = self.calc_vel(point["mp"], ref_point["mp"], self.s0D)
                    point["surr"]["ru"] = l
                    ref_point["surr"]["lo"] = -l

        for i in range(0, len(self.masspoints) ):
            row = self.masspoints[i]
            for j in range(0, len(row)):
                point = row[j]
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

        A.acc  = vector.obj(x = ((D.x * dSA.x)/A.mass), y = ((D.y * dSA.y)/A.mass ))
        B.acc  = vector.obj(x = ((D.x * dSB.x)/B.mass), y = ((D.y * dSB.y)/B.mass ))
        
        A.vel += self.dt * A.acc
        B.vel += self.dt * B.acc

        A.vel *= self.damping
        B.vel *= self.damping

        return dist
    
    def get_min(self, MP):
        minMag = -1
        minVec = vector.obj(x = -1, y = -1)
        for key in MP["surr"]:
             if type(MP["surr"][key]) != int:
                  vec = MP["surr"][key]
                  dist = self.length(vec)
                  if minMag == -1  or dist < minMag:
                       minMag = dist
                       minVec = MP["surr"][key]

        return {"mag": minMag, "vec": minVec}

    def self_collision(self, MP):
        rads = 2*self.radMass
        mins = self.get_min(MP)
        if mins["mag"] > -1 and mins["mag"] < rads:
            diffl = mins["mag"] - rads
            Acorr = mins["vec"].unit() * (.51*diffl)
            MP["mp"].pos += Acorr

            MP["mp"].vel =  -self.collisionDamp*MP["mp"].vel
        else:
             #MP["mp"].vel += self.dt * self.g
             MP["mp"].pos += self.dt * MP["mp"].vel 

    def collideWithLine(aL, bL, P):
        dirLine = bL - aL