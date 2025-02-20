from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNF, LEFT, GROUP, FUNS, FLUID, SOLID, PROPULSION

# Change `use_sfmath` to False to use computer modern
x = XDSM(use_sfmath=True)

#-------------------------DIAGONAL BLOCK DEFINITION--------------------------#
# Add optimizer
x.add_system("Optimizer", OPT, r"\text{IPOPT}")

# Add SU2_DEF block
x.add_system("SU2_DEF", FLUID, r"\text{SU2}\_\text{DEF}")

# Add SU2_CFD block
x.add_system("SU2_CFD", FLUID, r"\text{SU2}\_\text{CFD}")

# Add SU2_CFD_AD block
x.add_system("SU2_CFD_AD", FLUID, r"\text{SU2}\_\text{CFD}\_\text{AD}")

# Add SU2_DOT_AD block
x.add_system("SU2_DOT_AD", FLUID, r"\text{SU2}\_\text{DOT}\_\text{AD}")

# Add SU2_GEO block
x.add_system("SU2_GEO", FLUID, r"\text{SU2}\_\text{GEO}")

# Add propulsion block
#x.add_system("Func", FUNF, r"\text{Functions}", stack=True)
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

# IPOPT forward feed to SU2_DEF
x.connect("Optimizer", "SU2_DEF",r"\xi")

# SU2_DEF forward feed to SU2_CFD
x.connect("SU2_DEF", "SU2_CFD",r"\mathscr{X}")

# SU2_CFD forward feed to SU2_CFD_AD
x.connect("SU2_CFD", "SU2_CFD_AD",r"\mathscr{F}, \mathscr{X}")

# SU2_CFD_AD forward feed to SU2_DOT_AD
x.connect("SU2_CFD_AD", "SU2_DOT_AD",r"\mathscr{A}, \mathscr{X}")

# SU2_DEF forward feed to SU2_GEO
x.connect("SU2_DEF", "SU2_GEO",r"\xi, \mathscr{X}")


# SU2_DEF forward feed to func
#x.connect("SU2_DEF", "Func",r"\xi" )
# Func backward feed to SU2_DEF
#x.connect("Func", "SU2_CFD",r"\mathscr{X}")


# SU2_CFD forward feed to SU2_CFD_AD
#x.connect("SU2_CFD", "Func",r"x")
# Func backward feed to SU2_CFD_AD
#x.connect("Func", "SU2_CFD_AD",r"\mathscr{F}")

# SU2_CFD backward feed to IPOPT
x.connect("SU2_CFD", "Optimizer",r"f, g")

# SU2_CFD_AD forward feed to SU2_DOT_AD
#x.connect("SU2_CFD_AD", "Func",r"\mathscr{A}")
# Func backward feed to IPOPT
#x.connect("Func", "SU2_DOT_AD", r"\nabla f, \nabla g")


# Func output to IPOPT
x.connect("SU2_DOT_AD", "Optimizer",r"\nabla f, \nabla g")

# SU2_GEO forward feed to func
#x.connect("Func", "SU2_GEO", r"\mathfrak{X}")
#x.connect("SU2_GEO", "Func", r"\mathfrak{X}, \xi")
#x.connect("Func", "SU2_GEO", r"\mathfrak{G}")
x.connect("SU2_GEO", "Optimizer", r"h, \nabla h")
# Funch backward feed to IPOPT




#x.connect("SU2_CFD", "SU2_CFD_AD",r"\mathcal{R}(\mathscr{F})")
#x.connect("SU2_CFD_AD", "SU2_DOT_AD",r"\mathcal{R}(\mathscr{A})")
#x.connect("SU2_DOT_AD", "Func",r"\mathcal{R}(\mathscr{A})" )


#-------------------------INDIVIDUAL DISCIPLINES OUTPUT:BEGIN--------------------------#

x.add_output("Optimizer", r"\xi^*", side=LEFT)

#x.connect("Func", "Optimizer", r"f,g, \nabla f, \nabla g")
#-------------------------INDIVIDUAL DISCIPLINES OUTPUT:END--------------------------#


#-------------------------INDIVIDUAL DISCIPLINES INPUT:BEGIN--------------------------#
x.add_input("Optimizer", r"\xi^o")
#-------------------------INDIVIDUAL DISCIPLINES INPUT:END--------------------------#

x.add_process(['Optimizer', 'SU2_DEF', 'SU2_CFD', 'SU2_CFD_AD', 'SU2_DOT_AD', 'SU2_GEO', 'Optimizer'], arrow=False)

#x.add_process(['Optimizer', 'MDA', 'Func', 'Optimizer'], arrow=False)
x.write("aso")