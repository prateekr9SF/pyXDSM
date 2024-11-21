#from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNC, LEFT
import sys
sys.path.append("D:\pyXDSM-main\pyxdsm")
sys.path.append("D:\pyXDSM-main")
from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNF, LEFT, GROUP, FUNS, FLUID, SOLID, PROPULSION

# Change `use_sfmath` to False to use computer modern
x = XDSM(use_sfmath=True)

x.add_system("opt", OPT, r"\text{RunOptim.py}")
x.add_system("solver", SOLID, r"\text{Direct.py}")
x.add_system("D1", FUNS, r"\text{compute_center_of_gravity()}")
x.add_system("D2", FUNS, r"\text{sens_compliance()}")

#cx, cy, dcx_drho, dcy_drho = compute_center_of_gravity(nelx, nely, xPhys, node_coords, edofMat)
#obj, dc_drho = sens_compliance(u, edofMat, nelx, nely, KE, penal, xPhys, Emax, Emin)
x.connect("opt", "D1", "rho")
x.connect("opt", "D2", "rho")
x.connect("solver", "D1", "nelx,nely,xPhys,node_coords,edofMat")
x.connect("solver", "D2", "u, edofMat, nelx, nely, KE, penal, xPhys, Emax, Emin")
x.connect("D1", "solver", r"cx, cy, dcx_drho, dcy_drho")
x.connect("D2", "solver", "obj, dc_drho")


x.connect("D1", "opt", "cx, dcx_drho")
x.connect("D2", "opt", "obj, dc_drho")

x.add_output("opt", "rho*", side=LEFT)
x.add_output("D1", "cx*", side=LEFT)
x.add_output("D2", " obj*", side=LEFT)

x.write("TopOp",build=True)
