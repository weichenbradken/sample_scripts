atom_style granular
atom_modify map array
boundary f f f
newton off

communicate single vel yes

units si

region domain block 0.53 2.29 -4.8 4.8 -4.8 4.8  units box
create_box 3 domain
# 1: Ore, 2: Ball, 3: Shell liner



neighbor 0.02 bin
neigh_modify delay 0

fix m1 all property/global youngsModulus peratomtype 5e6 5e6 5e6
fix m2 all property/global poissonsRatio peratomtype 0.3 0.3 0.3
fix m3 all property/global coefficientRestitution peratomtypepair 3 0.3 0.3 0.3 &
                                                                    0.3 0.3 0.3 &
                                                                    0.3 0.3 0.3
fix m4 all property/global coefficientFriction peratomtypepair 3 0.5 0.3 0.5 &
                                                                 0.3 0.1 0.1 &
                                                                 0.5 0.1 0.0
#fix m5 all property/global coefficientRollingFriction peratomtypepair 3 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
#fix m6 all property/global cohesionEnergyDensity peratomtypepair 3 1e4 1e4 1e4 1e4 1e4 1e4 1e4 1e4 1e4
fix m7 all property/global k_finnie peratomtypepair 3 1.0 1.0 1.0 &
                                                      1.0 1.0 1.0 &
                                                      1.0 1.0 1.0

pair_style gran model hertz tangential history #cohesion sjkr rolling_friction cdt
pair_coeff * *

timestep 1e-4

fix gravi all gravity 9.81 vector 0.0 -1.0 0.0

#--------------------------------------------------------------------------------------------------------------------
#group shell_liner region domain
#group end_wall region domain

fix rotate all mesh/surface/stress file meshes/rotate.stl type 3 element_exclusion_list read element_exclusion_list_1.txt curvature 1e-6 wear finnie
fix cap all mesh/surface file meshes/cap.stl type 3 curvature 1e-6
fix granwalls1 all wall/gran model hertz tangential history mesh n_meshes 2 meshes rotate cap

#--------------------------------------------------------------------------------------------------------------------



#####################------------------------------------------------------------------------------------------------
group  ore region domain
group  ball  region domain

fix pts1 ore particletemplate/sphere 26483761 atom_type 1 density constant 2650 radius constant 0.06
fix pts2 ore particletemplate/sphere 15485863 atom_type 1 density constant 2650 radius constant 0.04
fix pts3 ore particletemplate/sphere 49979687 atom_type 1 density constant 2650 radius constant 0.03

fix pts4 ball particletemplate/sphere 15485867 atom_type 2 density constant 7850 radius constant 0.0625

fix pdd1 all particledistribution/discrete/massbased 62578189 4 pts1 0.017 pts2 0.05 pts3 0.07 pts4 0.863
#####################------------------------------------------------------------------------------------------------

###################################----------------------------------------------------------------------------------
region chrg mesh/tet file meshes/charge.vtk scale 1 move 0. 0. 0. rotate 0. 0. 0. units box side in

fix ins1 all insert/pack seed 94562057 distributiontemplate pdd1 &
 insert_every once overlapcheck yes volumefraction_region 0.25 &
 region chrg

fix integr all nve/sphere
###################################----------------------------------------------------------------------------------

#################################################--------------------------------------------------------------------
compute sp all erotate/sphere
#compute fc all pair/gran/local id force_normal force_tangential contactArea
#compute wfc all wall/gran/local id force_normal force_tangential contactArea
#compute ore_ball ore group/group ball
#compute ore_liner ore group/group shell_liner
#compute ore_ore ore group/group ore
#compute ball_liner ball group/group shell_liner
#compute ball_ball ball group/group ball

thermo_style custom step atoms ke c_sp vol
thermo 1000
thermo_modify lost ignore norm no
#################################################--------------------------------------------------------------------
run 1

##############################################################-------------------------------------------------------
dump dmp1 ore  custom 250 post/ore_*.liggghts  id type x y z vx vy vz radius
dump dmp2 ball custom 250 post/ball_*.liggghts id type x y z vx vy vz radius



#dump  dumpstl all mesh/stl 250 post/dump*.stl binary mesh1

dump dumpstress1 all mesh/gran/VTK 250 post/rotate_*.vtk stress wear rotate

#dump dmp_fc all local 250 post/fc_*.data c_fc[1] c_fc[2] c_fc[3] c_fc[4] c_fc[5] c_fc[6] c_fc[7] c_fc[8] c_fc[9] c_fc[10]
#dump dmp_wfc all local 250 post/wall_fc_*.data c_wfc[1] c_wfc[2] c_wfc[3] c_wfc[4] c_wfc[5] c_wfc[6] c_wfc[7] c_wfc[8] c_wfc[9] c_wfc[10]
#dump dmp_ore_ore all local 250 post/ore_ore_*.data c_ore_ore[1] c_ore_ore[2] c_ore_ore[3] c_ore_ore[4]
#dump dmp_ball_liner all local 250 post/ball_liner_*.data c_ball_liner[1] c_ball_liner[2] c_ball_liner[3] c_ball_liner[4]
#dump dmp_ball_ball all local 250 post/ball_ball_*.data c_ball_ball[1] c_ball_ball[2] c_ball_ball[3] c_ball_ball[4]
##############################################################-------------------------------------------------------

fix move1 all move/mesh mesh rotate rotate origin 0.0 0.0 0.0 axis 1.0 0.0 0.0 period 5.88

variable tqX equal f_rotate[4]
variable tqY equal f_rotate[5]
variable tqZ equal f_rotate[6]
fix csvfile all print 250 "${tqX},${tqY},${tqZ}" screen no file mill_torque.csv

run 294000
unfix move1
