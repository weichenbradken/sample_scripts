#bond

atom_style	granular bond/gran n_bondtypes 1 bonds_per_atom 6
#atom_style	granular
atom_modify	map array
boundary	f f f
newton		off

#processors  2 1 1

communicate	single vel yes

units		si

region		reg block -2.1 2.1 -1 3.1 -2.1 2.1 units box
create_box	2 reg #bonds 1 6

neighbor	0.002 bin
neigh_modify	delay 0

#New pair style
pair_style 	gran model hertz tangential history
pair_coeff	* *

#bond
bond_style 	gran

variable	simplebreak equal 0
variable	stressbreak equal 1

fix 		m1 all property/global youngsModulus peratomtype 1.e7 1.e7
fix 		m2 all property/global poissonsRatio peratomtype 0.3 0.3
fix 		m3 all property/global coefficientRestitution peratomtypepair 2 0.2 0.2 0.2 0.2
fix 		m4 all property/global coefficientFriction peratomtypepair 2 0.3 0.3 0.3 0.3

timestep	0.00001
fix		gravi all gravity 9.81 vector 0.0 -1.0 0.0

fix  convave all mesh/surface file meshes/concave.stl type 2 element_exclusion_list write exclusion1.txt curvature 1e-6
fix  mantle all mesh/surface file meshes/mantle.stl type 2 element_exclusion_list write exclusion2.txt curvature 1e-6
fix	 walls all wall/gran model hertz tangential history mesh n_meshes 2 meshes convave mantle
#for simplebreak
#bond_coeff 	1 0.0025 10000000000 10000000000 ${simplebreak} 0.002501
#for stressbreak
bond_coeff 	1 1 1e8 1e8 ${stressbreak} 1e4 1e4

# ==============================================================
# create particles IN A DEFINED REGION to collide against a wall
# ==============================================================
#region		bc mesh/tet file sphere_fine.vtk scale 0.05 move 1 1 1 rotate 0. 0. 0.  units box #scale 0.05 move 0.05 0.05 0.05  rotate 0. 0. 0. units box
#region bc sphere 0.1 0.1 0.1 0.05 units box
#lattice		sc 0.005
#create_atoms	1 region bc
#group		bonded region bc
#set		group all density 2500 diameter 0.005 
#set		group all vz 0 vx 0

group multispheres initialize 


fix		pts1 multispheres particletemplate/multisphere 15485863 atom_type 1&
         density constant 2000 nspheres 10 ntry 1000 spheres file data/stone1.multisphere scale 0.007 type 1

region	chrg mesh/tet file meshes/charge.vtk scale 1 move 0. 0. 0. rotate 0. 0. 0. units box side in

fix    ins1 all insert/pack seed 15488647 distributiontemplate pdd1 &
       insert_every once overlapcheck yes volumefraction_region 0.5&
       region chrg

###TODO blow the particles up (see examples/LIGGGHTS/Tutorial_Public/packing/###

#Material properties required for new pair styles
#mass 		1 1.0 #dummy

fix 		bondcr all bond/create/gran 1 1 1 0.0051 1  6

#fix		top	all mesh/surface file	top.stl		type 1     #move 0.05 0.05 0.2
#fix		bottom	all mesh/surface file	bottom.stl	type 1 	   #move 0.05 0.05 0.05
#region and insertion
#group		nve_group region reg

#apply nve integration to all particles that are inserted as single particles
fix intMulti multispheres multisphere

#output settings, include total thermal energyg
#compute		1 all erotate/sphere
#variable	etotal equal ke+c_1
fix				ts all check/timestep/gran 1000 0.1 0.1
thermo_style	custom step atoms numbond
thermo		1000
thermo_modify	lost ignore norm no
compute_modify	thermo_temp dynamic yes

#insert the first particles so that dump is not empty
#shell mkdir post
dump		dmp 	all custom   100 post/dump*.liggghts id type x y z vx vy vz fx fy fz omegax omegay omegaz radius
dump 		dumpstl all mesh/stl 100 post/dump*.stl

#compute b1 all property/local batom1x batom1y batom1z batom2x batom2y batom2z batom1 batom2 btype
#dump 	bnd all local 100 post/bonds*.bond c_b1[1] c_b1[2] c_b1[3] c_b1[4] c_b1[5] c_b1[6] c_b1[7] c_b1[8] c_b1[9]

#insert particles
run		1
fix_modify	bondcr every 0

# ================================================
# after the bonds are formed,
# exclude pairwise interaction ?
# ================================================
#neigh_modify	exclude group bonded bonded

#run

fix		movecad1 all move/mesh mesh top  linear 0 0 -0.5

run		10000 

#run		3500 upto
#dump_modify	dmp every 5
#run		500
