from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNF, LEFT, GROUP, FUNS, FLUID, SOLID, PROPULSION, EMISSIONS

# Change `use_sfmath` to False to use computer modern
x = XDSM(use_sfmath=True)

#-------------------------DIAGONAL BLOCK DEFINITION--------------------------#
# Add optimizer
x.add_system("Optimizer", OPT, r"\text{Optimizer}")

# Add MDA block
x.add_system("MDA", SOLVER, r"\text{MDA}")

# Add fluid block
x.add_system("Fluid", FLUID, r"\text{Aerodynamics}")

# Add solid block
x.add_system("Solid", SOLID, r"\text{Structures}")

# Add propulsion block
x.add_system("Prop", PROPULSION, r"\text{Propulsion}")

# Add propulsion block
x.add_system("Func", FUNF, r"\text{Functions}", stack=True)

# Add emissions block
#x.add_system("Ems", EMISSIONS, r"\text{Env. metric}")
#-------------------------DIAGONAL BLOCK DEFINITION:END--------------------------#

#-------------------------SUB-FUNCTION BLOCK DEFINITION--------------------------#

# Add fluid sub-function
#x.add_system("fluid_sub_func", FUNF, r"\text{traction()}")

# Add solid sub-function
#x.add_system("solid_sub_func", FUNS, r"\text{displacement()}")


#-------------------------OFF-DIAGONAL BLOCK DEFINITION:END--------------------------#

# DEFINE CONECTIONS

# Fluid passes mesh coordinates x, y, z to traction()
#x.connect("Fluid", "fluid_sub_func", r"\text{x,y,z}")


# Fluid sub func passes traction to solid
#x.connect("fluid_sub_func", "Solid", r"f_x, f_y, f_z")

# Solid passes tractions to internal solver
#x.connect("Solid", "solid_sub_func", r"f_x, f_y, f_z")

# Solid internal solver passes nodal displacements to fluid
#x.connect("solid_sub_func", "Fluid", r"u_x, u_y, u_z")

# Solid passes elastic residual to MDA
#x.connect("Solid", "MDA", r"\mathcal{S}")

# Fluid passes fluid residual to MDA
#x.connect("Fluid", "MDA", r"\mathcal{F}")

# IPOPT Reached out to MDA solver
x.connect("Optimizer", "Fluid","x^o, x_a" )
x.connect("Optimizer", "Solid","x^o, x_s" )
x.connect("Optimizer", "Prop","x^o, x_p" )
#x.connect("Optimizer", "Func","x" )

# MDA passes all states to emissions
#x.connect("MDA", "FuncE", "y_a,y_s,y_p")

# Emissions returns sensitivities to optimizer
#x.connect("FuncE", "Optimizer", r" e, \nabla e")


# MDA passes structural and propulsion variables to fluid
x.connect("MDA", "Fluid", "u_s,u_p")

# MDA passespropulsion variables to solid
x.connect("MDA", "Solid", "u_p")

# Fluid passes aerodynamic variables to elastic and propulsion
x.connect("Fluid", "Solid", "u_a")
x.connect("Fluid", "Prop", "u_a")

# Solid passes elastic variable to propulsion
x.connect("Solid", "Prop", "u_s")

# Fluid passes aerodynamic variable to MDA
x.connect("Fluid", "MDA", "u_a")

# Solid passes aerodynamic variable to MDA
x.connect("Solid", "MDA", "u_s")

# Solid passes aerodynamic variable to MDA
x.connect("Prop", "MDA", "u_p")

# All components' converged state passed to Emissions
#x.connect("MDA", "Ems", "u_a^*, u_s^*, u_p^*")



# Fluid passes converged aerodynamic variable to Functions
x.connect("Fluid", "Func", "u_a^*")
x.connect("Solid", "Func", "u_s^*")
x.connect("Prop", "Func", "u_p^*")




#-------------------------INDIVIDUAL DISCIPLINES OUTPUT:BEGIN--------------------------#
x.add_output("Fluid", "u_a^*", side=LEFT)
x.add_output("Solid", "u_s^*", side=LEFT)
x.add_output("Prop", "u_p^*", side=LEFT)
x.add_output("Optimizer", "x^*", side=LEFT)

x.connect("Func", "Optimizer", r"J, g, h, c, \nabla J, \nabla g, \nabla h, \nabla c")
#x.connect("Ems", "Optimizer", r"J, g, h, c, \nabla J, \nabla g, \nabla h, \nabla c")
#-------------------------INDIVIDUAL DISCIPLINES OUTPUT:END--------------------------#


#-------------------------INDIVIDUAL DISCIPLINES INPUT:BEGIN--------------------------#
x.add_input("Optimizer", "x^o")
#-------------------------INDIVIDUAL DISCIPLINES INPUT:END--------------------------#

x.add_process(['Optimizer', 'MDA', 'Fluid', 'Solid', 'Prop', 'MDA'], arrow=False)

x.add_process(['Optimizer', 'MDA', 'Func'], arrow=False)

#x.add_process(['Optimizer', 'MDA', 'Func', 'Optimizer'], arrow=False)

x.write("mdao")