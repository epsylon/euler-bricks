#!/usr/bin/env python3 
# -*- coding: utf-8 -*-"
"""
Euler-Bricks - 2020 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with Euler-Bricks; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import os, sys, math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt

plt.rcParams.update({'figure.max_open_warning': 0})

class EulerBrick(object):
    def __init__(self):
        self.store_bricks = "bricks/"

    def banner(self):
        print(75*"=")
        print("  _____      _           ____       _      _         ")
        print(" | ____|   _| | ___ _ __| __ ) _ __(_) ___| | _____  ")
        print(" |  _|| | | | |/ _ \ '__|  _ \| '__| |/ __| |/ / __| ")
        print(" | |__| |_| | |  __/ |  | |_) | |  | | (__|   <\__ \ ")
        print(" |_____\__,_|_|\___|_|  |____/|_|  |_|\___|_|\_\___/ ")
        print("                                                     ")
        print(75*"=","\n")
        print(" Does a 'perfect cuboid' exist?\n")
        print(75*"=","\n")

    def run(self, opts=None):
        self.banner()
        self.mode=input(" -Set mode: manual (default), learning (M/l): ") 
        self.root=input(" -Set range (ex: 1-1000 or 1000-1000000 (PRESS ENTER = 1-1000) (STOP = CTRL+z): ")
        if not self.root:
            self.root="1-1000"
        print("\n[Info] Looking for 'bricks' in the range: "+ str(self.root)+ "\n")
        self.generate_bricks(self.root)

    def generate_bricks(self, rng):
        srng = rng.split('-')
        try:
            minrange=int(srng[0]) 
            maxrange=int(srng[1])
        except:
            print(40*"-"+"\n")
            print("[Error] Numbers on range should be integers (ex: 1-1000). Aborting...\n")
            sys.exit(2)
        if minrange < maxrange:
            pass
        else:
            print(40*"-"+"\n")
            print("[Error] Min range should be minor than max range (ex: 1-1000). Aborting...\n")
            sys.exit(2)
        self.init = int(minrange) 
        self.end = int(maxrange)
        n = 1
        if not os.path.exists(self.store_bricks):
            os.mkdir(self.store_bricks)
        for a in range(self.init, self.end):
            asq = a**2
            for b in range(a, self.end):
                bsq = b**2
                d = math.sqrt(asq + bsq)
                if not d.is_integer():
                    continue
                for c in range(b, self.end):
                    n = n + 1
                    csq = c**2
                    e = math.sqrt(asq + csq)
                    if not e.is_integer():
                        continue
                    f = math.sqrt(bsq + csq)
                    if not f.is_integer():
                        continue
                    print(40*"-"+"\n")
                    print("[Info] Found 'brick'!!\n")
                    print(" -ID: {} ({})".format(n, str(c)+':'+str(b)+':'+str(a)))
                    print(" -Hedges: X={} Y={} Z={}".format(int(c), int(b), int(a)))
                    print(" -Diagonals: dZY={} dXZ={} dXY={}".format(int(d), int(e), int(f)))
                    self.draw(a,b,c,d,e,f,n)

    def draw(self, a, b, c, d, e, f, n):
        points = np.array([[c, b, a],
                  [c, -b, -a],
                  [c, b, -a ],
                  [-c, b, -a],
                  [-c, -b, a],
                  [c, -b, a ],
                  [c, b, a  ],
                  [-c, b, a]])
        P = [[2.06498904e-01 , -6.30755443e-07 ,  1.07477548e-03],
            [1.61535574e-06 ,  1.18897198e-01 ,  7.85307721e-06],
            [7.08353661e-02 ,  4.48415767e-06 ,  2.05395893e-01]]
        Z = np.zeros((8,3))
        for i in range(8): Z[i,:] = np.dot(points[i,:],P)
        Z = 1*Z
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        r = [-1,1]
        X, Y = np.meshgrid(r, r)
        ax.scatter3D(Z[:, 0], Z[:, 1], Z[:, 2])
        verts = [[Z[0],Z[1],Z[2],Z[3]],
                [Z[4],Z[5],Z[6],Z[7]], 
                [Z[0],Z[1],Z[5],Z[4]], 
                [Z[2],Z[3],Z[7],Z[6]], 
                [Z[1],Z[2],Z[6],Z[5]],
                [Z[4],Z[7],Z[3],Z[0]]]
        verts2 = [[-Z[0],-Z[1],-Z[2],-Z[3]],
                [-Z[4],-Z[5],-Z[6],-Z[7]], 
                [-Z[0],-Z[1],-Z[5],-Z[4]], 
                [-Z[2],-Z[3],-Z[7],-Z[6]], 
                [-Z[1],-Z[2],-Z[6],-Z[5]],
                [-Z[4],-Z[7],-Z[3],-Z[0]]]
        ax.add_collection3d(Poly3DCollection(verts, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
        ax.add_collection3d(Poly3DCollection(verts2, facecolors='cyan', linewidths=0, edgecolors='r', alpha=.25))
        ax.set_xlabel("X: {} dXY: {} dXZ: {}".format(int(c),int(f),int(e)))
        ax.set_ylabel("Y: {} dYX: {} dYZ: {}".format(int(b),int(f),int(d)))
        ax.set_zlabel("Z: {} dZX: {} dZY: {}".format(int(a),int(e),int(d)))
        ax.w_xaxis.set_ticklabels("")
        ax.w_yaxis.set_ticklabels("")
        ax.w_zaxis.set_ticklabels("")
        header = "[{}".format("x:"+str(c)+' y:'+str(b)+' z:'+str(a) + "]\n")
        fig.canvas.set_window_title("Euler's brick ID: {} ".format(n))
        plt.title(header)
        if not os.path.exists(self.store_bricks+str(a)+'_'+str(b)+'_'+str(c)+"-euler_brick.png"):
            fig.savefig(self.store_bricks+str(c)+'_'+str(b)+'_'+str(a)+"-euler_brick.png")
            print("\n[Info] Generated 'brick' image at: "+self.store_bricks+str(c)+'_'+str(b)+'_'+str(a)+"-euler_brick.png\n")
        else:
            print("\n[Info] You have previously saved this 'brick'...\n")
        if not self.mode == "l" or self.mode == "L" or self.mode == "Learn" or self.mode == "learn":
            plt.show()
        ax.clear()

if __name__ == "__main__":
    app = EulerBrick()
    app.run()
