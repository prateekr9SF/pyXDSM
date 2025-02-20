from pyxdsm.XDSM import XDSM, OPT, SOLVER, FUNF, LEFT, GROUP, FUNS, FLUID, SOLID, PROPULSION

# Change `use_sfmath` to False to use computer modern
x = XDSM(use_sfmath=True)

#-------------------------DIAGONAL BLOCK DEFINITION--------------------------#

# Add MDAS block
x.add_system("MDAS", OPT, r"\text{MDAS}")

# Add Fuselage block
x.add_system("Fuse", FLUID, r"\text{Fuselage}")

# Add Wing block
x.add_system("Wing", FLUID, r"\text{Wing}")

# Add tail block
x.add_system("Tail", FLUID, r"\text{H/V Tail}")

# Define aircraft balance block
x.add_system("baln", SOLVER, r"\text{Balance}")

# Add solid block
x.add_system("drag", SOLID, r"\text{Drag}")

# Add propulsion block
x.add_system("Eng", FLUID, r"\text{Engine}")

# Add propulsion block
x.add_system("Mission", PROPULSION, r"\text{Mission}")

# Add initial call functions
x.add_system("Ini_Func", FUNF, r"\text{initialize()}", stack=True)


# Fuselage functions
x.add_system("size_Func", FUNF, r"\text{structures()}", stack=True)

# Wing functions
x.add_system("eng_Func", FUNF, r"\text{engine()}", stack=True)

# Engine functions
x.add_system("aero_Func", FUNF, r"\text{aero()}", stack=True)

# Mission functions
x.add_system("mission_Func", FUNF, r"\text{trajectory()}", stack=True)

# Balance functions
x.add_system("bal_Func", FUNF, r"\text{stability()}", stack=True)


#-------------------------DIAGONAL BLOCK DEFINITION:END--------------------------#

# MDAS unpacks and initializes values
x.connect("MDAS", "Ini_Func", "x_a^o, x_s^o, x_p^o")

# Initialized functions pass values back to MDAS
x.connect("Ini_Func", "MDAS", "x_a^t,x_s^t,x_p^t")

##------------WING--------------##
# MDAS passes variables to Wing
x.connect("MDAS", "Wing", "x_a^i, x_s^i")

# Forward feed to aero and structures
x.connect("Wing", "aero_Func", "x_a^i")
x.connect("Wing", "size_Func", "x_s^i")

# Backward feed to wing
x.connect("aero_Func","Wing", "y_a^i")
x.connect("size_Func","Wing", "y_s^i")
##----------------------------------##


##------------FUSELAGE--------------##
# MDAS passes variabels to fuselage
x.connect("MDAS", "Fuse", "x_a^i,x_s^i")

# Forward feed to aero and structures
x.connect("Fuse", "aero_Func", "x_a^i")
x.connect("Fuse", "size_Func", "x_s^i")

# Backward feed to fuselage
x.connect("aero_Func", "Fuse", "y_a^i")
x.connect("size_Func","Fuse", "y_s^i")
##----------------------------------##

##------------TAIL--------------##
# MDAS passes variables to Tail
x.connect("MDAS", "Tail", "x_a^i, x_s^i")

# Forward feed to aero and structures
x.connect("Tail", "aero_Func", "x_a^i")
x.connect("Tail", "size_Func", "x_s^i")

# Backward feed to tail
x.connect("aero_Func","Wing", "y_a^i")
x.connect("size_Func","Wing", "y_s^i")
##----------------------------------##

##------------BALANCE---------------##
# MDA passes  propulsion variables to balance
x.connect("MDAS", "baln", "x_p^i")

# Fuselage, tail and wing pass variables to balance
x.connect("Fuse", "baln", "x_a^i, x_s^i")
x.connect("Wing", "baln", "x_a^i, x_s^i")
x.connect("Tail", "baln", "x_a^i, x_s^i")

# Forward feed to stability functions
x.connect("baln", "bal_Func", "x_a^i, x_s^i, x_p^i")

# Backward feed to balance
x.connect("bal_Func", "baln", "y_a^i, y_s^i, y_p^i")
##----------------------------------##

##------------DRAG---------------##
# Balance passes variables to drag
x.connect("baln", "drag", "x_a^i, x_s^i, x_p^i")

# Forward feed to aero functions
x.connect("drag", "aero_Func", "x_a^i, x_s^i, x_p^i")

# Backward feed to drag
x.connect("aero_Func", "drag", "y_a^i, y_s^i, y_p^i")
##----------------------------------##

##-------------ENGINE--------------##
# MDAS passes variables to engine
x.connect("MDAS", "Eng",  "x_p^i")

# Balance passes structures variabels to engine
x.connect("baln", "Eng", "x_s^i")

# Drag passes aerodynamic variabels to engine
x.connect("drag", "Eng", "x_a^i")

# Forward feed to engine functions
x.connect("Eng", "eng_Func",  "x_p^i")

# Backward feed to engine functions
x.connect("eng_Func", "Eng",  "y_p^i")
##----------------------------------##

##------------MISSION---------------##
# Drag passes variables to mission
x.connect("drag", "Mission", "x_a^i, x_s^i")

# Engine passes variabels to mission
x.connect("Eng", "Mission", "x_p^i")

# Forward feed to trajectory functions
x.connect("Mission", "mission_Func", "x_a^i, x_s^i, x_p^i")

# Backward feed to mission
x.connect("mission_Func", "Mission", "y_a^i, y_s^i, y_p^i")

# Mission computes fuel burn for trajectory and passes back to MDAS
x.connect("Mission", "MDAS", "W_{MTO}, W_{Fuel}, x_a^i, x_s^i, x_p^i")

#-------------------------INDIVIDUAL DISCIPLINES OUTPUT:BEGIN--------------------------#
x.add_output("MDAS", "MTOW^*", side=LEFT)

#-------------------------INDIVIDUAL DISCIPLINES OUTPUT:END--------------------------#


#-------------------------INDIVIDUAL DISCIPLINES INPUT:BEGIN--------------------------#
x.add_input("MDAS", "x_a^o, x_s^o, x_p^o")
#-------------------------INDIVIDUAL DISCIPLINES INPUT:END--------------------------#

# OUTER ITERATION PROCESS
x.add_process(['MDAS', 'Ini_Func', 'MDAS'], arrow=False)

# INNER ITERATION PROCESS
x.add_process(['MDAS', 'Fuse'], arrow=False)
x.add_process(['MDAS', 'Wing'], arrow=False)
x.add_process(['MDAS', 'Tail'], arrow=False)
x.add_process(['Tail', 'baln'], arrow=False)
x.add_process(['Fuse', 'baln'], arrow=False)
x.add_process(['baln', 'drag'], arrow=False)
x.add_process(['MDAS', 'Eng'], arrow=False)
x.add_process(['drag', 'Eng'], arrow=False)
x.add_process(['drag', 'Mission'], arrow=False)
x.add_process(['Eng', 'Mission'], arrow=False)
x.add_process(['Mission', 'MDAS'], arrow=False)


#x.add_process(['Optimizer', 'MDAS', 'Func', 'Optimizer'], arrow=False)

x.write("mdas")