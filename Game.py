"""
0.0:	target_mass
0.1:	target_charge
0.2.x:	target_coordinate
0.3.x:	target_axial_velocity
1.0:	source_mass
1.1:	source_charge
1.2.x:	source_coordinate
1.3.x:	source_axial_velocity
"""
import pygame
import Radial_Object as RO
import surface as SU
import physics as phy
import custom_math as m2
import math
import random

def make_triangle(centre):
	Thita=random.random()*2*math.pi
	point1=[centre[0]+40*math.sin(Thita), centre[1]+40*math.cos(Thita)]
	point2=[centre[0]+40*math.sin(2*math.pi/3+Thita), centre[1]+40*math.cos(2*math.pi/3+Thita)]
	point3=[centre[0]+40*math.sin(4*math.pi/3+Thita), centre[1]+40*math.cos(4*math.pi/3+Thita)]
	next_surface_list=[]
	next_surface_list.append(SU.Surface([point1, point2], 2))
	next_surface_list.append(SU.Surface([point2, point3], 2))
	next_surface_list.append(SU.Surface([point3, point1], 2))
	return next_surface_list

render_time_step=1/float(input("Enter Monitor Refresh Rate: "))

pygame.init()
infoObject = pygame.display.Info()
pygame.display.set_caption("Test Environment")
screen = pygame.display.set_mode((infoObject.current_w, int(infoObject.current_w/2)))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

width = infoObject.current_w
height = infoObject.current_w/2
running = True
Radial_Object_List = [RO.Radial_Object([width/2, height/2-50], [0, 0], 50*22474266964325.848, 0, 10, False, [0,255,0])]
Surface_List = []
Physics_Model_List = [phy.newtonian_physics_model()]
Gravity_List = [Physics_Model_List[i].Get_Gravity() for i in range(len(Physics_Model_List))]
Surface_List.append(SU.Surface([[0, 0], [width-1, 0]], 2))
Surface_List.append(SU.Surface([[width/2-400, height/2], [width/2+400, height/2]], 2))
Surface_List.append(SU.Surface([[width/2-400, height/2-20], [width/2-400, height/2+20]], 2))
Surface_List.append(SU.Surface([[width/2+400, height/2-20], [width/2+400, height/2+20]], 2))
Surface_List.append(SU.Surface([[width/2, height/2-200], [width/2, height/2+200]], 2))
Surface_List.append(SU.Surface([[width/2-20, height/2-200], [width/2+20, height/2-200]], 2))
Surface_List.append(SU.Surface([[width/2-20, height/2+200], [width/2+20, height/2+200]], 2))
Surface_List.append(SU.Surface([[width-1, 0], [width-1, height-1]], 2))
Surface_List.append(SU.Surface([[width-1, height-1], [0, height-1]], 2))
Surface_List.append(SU.Surface([[0, 0], [0, height-1]], 2))
physics_prev_time=0
render_prev_time=0
player_hit=False

while running:
	physics_time_step=pygame.time.get_ticks()/1000-physics_prev_time
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	while(len(Radial_Object_List)<5+(render_prev_time//15) and (not player_hit)):
		rand=random.random()
		if(rand<0.25):
			Radial_Object_List.append(RO.Radial_Object([width/4-200+400*random.random(), height/4-100+200*random.random()], [100*random.random(), 100*random.random()], 15*22474266964325.848, 0, 15, False, [40+215*random.random(),40+215*random.random(),40+215*random.random()]))
			Surface_List.extend(make_triangle([3*width/4-200+400*random.random(), 3*height/4-100+200*random.random()]))
		elif(rand<0.5):
			Radial_Object_List.append(RO.Radial_Object([width/4-200+400*random.random(), 3*height/4-100+200*random.random()], [100*random.random(), 100*random.random()], 15*22474266964325.848, 0, 15, False, [40+215*random.random(),40+215*random.random(),40+215*random.random()]))
			Surface_List.extend(make_triangle([3*width/4-200+400*random.random(), height/4-100+200*random.random()]))
		elif(rand<0.75):
			Radial_Object_List.append(RO.Radial_Object([3*width/4-200+400*random.random(), 3*height/4-100+200*random.random()], [100*random.random(), 100*random.random()], 15*22474266964325.848, 0, 15, False, [40+215*random.random(),40+215*random.random(),40+215*random.random()]))
			Surface_List.extend(make_triangle([width/4-200+400*random.random(), height/4-100+200*random.random()]))
		else:
			Radial_Object_List.append(RO.Radial_Object([3*width/4-200+400*random.random(), height/4-100+200*random.random()], [100*random.random(), 100*random.random()], 15*22474266964325.848, 0, 15, False, [40+215*random.random(),40+215*random.random(),40+215*random.random()]))
			Surface_List.extend(make_triangle([width/4-200+400*random.random(), 3*height/4-100+200*random.random()]))
	
	if(not (physics_time_step==0 or player_hit)):
		print(1/physics_time_step)
		physics_prev_time=pygame.time.get_ticks()/1000
		radial_object_counter=0
		for i in Radial_Object_List:
			force = [0, 0]
			values = {
			"0.0": i.mass,
			"0.1": i.charge 
			}
			for j in range(Physics_Model_List[0].dimensions):
				values["0.2."+str(j)] = i.position[j]
			for j in range(Physics_Model_List[0].dimensions):
				values["0.3."+str(j)] = i.velocity[j]
			if(not radial_object_counter==0):
				for j in Radial_Object_List:
					if not j == i:
						values["1.0"] = j.mass
						values["1.1"] = j.charge
						for k in range(Physics_Model_List[0].dimensions):
							values["1.2."+str(k)] = j.position[k]
						for k in range(Physics_Model_List[0].dimensions):
							values["1.3."+str(k)] = j.velocity[k]
						temp = [Gravity_List[0][i](values) for i in range(len(Gravity_List[0]))]
						force = [force[i]+temp[i] for i in range(len(temp))]
			else:
				dist=m2.dist(pygame.mouse.get_pos(),i.position)
				i.velocity[0]=1500*(pygame.mouse.get_pos()[0]-i.position[0])/dist
				i.velocity[1]=1500*(pygame.mouse.get_pos()[1]-i.position[1])/dist
				
			radial_object_counter+=1
			
			Physics_Model_List[0].Update_Kinematics(i, force=force, time_step=physics_time_step)
		
		Physics_Model_List[0].Surface_Collision(Radial_Object_List, Surface_List, time_step=physics_time_step)
		player_hit=Physics_Model_List[0].Radial_Object_Collision(Radial_Object_List, time_step=physics_time_step)
	
	render_time_delay=pygame.time.get_ticks()/1000-render_prev_time
	if(render_time_delay>=render_time_step):
		render_prev_time+=render_time_delay
		text = font.render("Score: "+str(physics_prev_time), True, (0,255,0))
		screen.fill((0, 0, 0))
		screen.blit(text, (20, 20))
		pygame.draw.circle(screen, Radial_Object_List[0].color, Radial_Object_List[0].position, Radial_Object_List[0].radius, width=5)
		for i in Radial_Object_List[1:]:
			pygame.draw.circle(screen, i.color, i.position, i.radius)
		for i in Surface_List:
			pygame.draw.line(screen,(255,255,255),i.points[0],i.points[1],1)
		pygame.display.update()
