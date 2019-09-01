"""
@author Dhruv
@date July 3, 2018
@version 5
"""
from opentrons import containers,labware, instruments, robot

robot.head_speed(x=600, y=600, z=125)  # Head speed of the robot in mm/s. Max is 600 for X and Y. 125 for Z


m300rack_1   = containers.load('tiprack-200ul', '1')
m300rack_2   = containers.load('tiprack-200ul', '4')


from sqlite3 import IntegrityError
try:
    custom_container = labware.create(
    '4x6_Tube_rack',            # name of you container
    grid=(6, 4),                # specify amount of (columns, rows)
    spacing=(19.5, 19.5),       # distances (mm) between each (column, row)
    diameter=3.5,              # diameter (mm) of each well on the plate (was 10.6)
    depth=40)                   # depth (mm) of each well on the plate

except IntegrityError:
    pass

try:
    custom_container = labware.create(
    'plate_6_well',            # name of you container
    grid=(3, 2),                # specify amount of (columns, rows)
    spacing=(39.12,39.12),       # distances (mm) between each (column, row)
    diameter=10,                # diameter (mm) of each well on the plate (was 35)
    depth=17.4)                   # depth (mm) of each well on the plate

except IntegrityError:
    pass
plate_6_well_1= containers.load('plate_6_well', '2')
plate_6_well_2= containers.load('plate_6_well', '3')

# The Operator Must know how many Tube racks they are going to need depending on the volumes they are specifying
# Tuberacks should go in the following slots in order. Slot 2 , 3 , 6 , 7 , 8 , 9. for easy of use
# Slot 5 is reseved for the 6-well-plate. (To increase transfer Efficiency)
tube_rack =[]
tube_rack.append(containers.load('4x6_Tube_rack', '5'))
tube_rack.append(containers.load('4x6_Tube_rack', '6'))
tube_rack.append(containers.load('4x6_Tube_rack', '7'))
tube_rack.append(containers.load('4x6_Tube_rack', '8'))
tube_rack.append(containers.load('4x6_Tube_rack', '9'))
tube_rack.append(containers.load('4x6_Tube_rack', '10'))



p50 = instruments.P50_Single(mount="left",tip_racks=[m300rack_1],dispense_flow_rate= 40)
p300 = instruments.P300_Single(mount="right",tip_racks=[m300rack_2],dispense_flow_rate=80)

# Components are arranged in columns. (Top to bottom and left to right).Total 6 Components
# Components should be labeled in order-> A1, B1, A2, B2, A3, B3 for ease of use
All_Component=[]
All_Component.append(plate_6_well_1.wells('A1'))
All_Component.append(plate_6_well_1.wells('B1'))
All_Component.append(plate_6_well_1.wells('A2'))
All_Component.append(plate_6_well_1.wells('B2'))
All_Component.append(plate_6_well_1.wells('A3'))
All_Component.append(plate_6_well_1.wells('B3'))
All_Component.append(plate_6_well_2.wells('A1'))
All_Component.append(plate_6_well_2.wells('B1'))
All_Component.append(plate_6_well_2.wells('A2'))
All_Component.append(plate_6_well_2.wells('B2'))
All_Component.append(plate_6_well_2.wells('A3'))
All_Component.append(plate_6_well_2.wells('B3'))


WELLS =[[['A1','B1','C1','D1','A2','B2','C2','D2','A3','B3','C3','D3','A4','B4','C4','D4','A5','B5','C5','D5','A6','B6','C6','D6'],['A1','B1','C1']],[['A1','B1','C1','D1','A2','B2','C2','D2','A3','B3','C3','D3','A4','B4','C4','D4','A5','B5','C5','D5','A6','B6','C6','D6'],['A1','B1','C1']],[['A1','B1','C1','D1','A2','B2','C2','D2','A3','B3','C3','D3','A4','B4','C4','D4','A5','B5','C5','D5','A6','B6','C6','D6'],['A1','B1','C1']],[['A1','B1','C1','D1','A2','B2','C2','D2','A3','B3','C3','D3','A4','B4','C4','D4','A5','B5','C5','D5','A6','B6','C6','D6'],['A1','B1','C1']],[['A1','B1','C1','D1','A2','B2','C2','D2','A3','B3','C3','D3','A4','B4','C4','D4','A5','B5','C5','D5','A6','B6','C6','D6'],['A1','B1','C1']],[['A1','B1','C1','D1','A2','B2','C2','D2','A3','B3','C3','D3','A4','B4','C4','D4','A5','B5','C5','D5','A6','B6','C6','D6'],['A1','B1','C1']]]


VOLUMES = [[[11.2,11.2,11.2,11.2,5.6,16.8,5.6,16.8,11.2,11.2,11.2,11.2,5.6,5.6,16.8,16.8,5.6,5.6,16.8,16.8,11.2,11.2,11.2,11.2],[11.2,11.2,11.2]],[[5,5,15,15,10,10,10,10,10,10,10,10,5,15,5,15,10,10,10,10,5,15,5,15],[10,10,10]],[[80.0857,22.9429,70.0857,12.9429,59.6143,48.4143,44.6143,33.4143,82.5857,25.4429,67.5857,10.4429,57.1143,47.1143,45.9143,35.9143,80.6857,23.5429,69.4857,12.3429,59.0143,49.0143,44.0143,34.0143],[46.5143,46.5143,46.5143]],[[15,15,15,15,7.5,7.5,22.5,22.5,7.5,7.5,22.5,22.5,15,15,15,15,15,15,15,15,7.5,7.5,22.5,22.5],[15,15,15]],[[85.71429,142.8571,85.71429,142.8571,114.2857,114.2857,114.2857,114.2857,85.71429,142.8571,85.71429,142.8571,114.2857,114.2857,114.2857,114.2857,85.71429,142.8571,85.71429,142.8571,114.2857,114.2857,114.2857,114.2857],[114.2857,114.2857,114.2857]],[[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,3]]]


def sort_volume_n_well(Comp_Volume,Comp_well):
    #Sorts the points in Volume list first and also sorts the wells accordingly, after that sorts the wells.
    points = zip(Comp_Volume,Comp_well)
    sorted_points = sorted(points)
    Comp_Volume = [point[0] for point in sorted_points if point[0] != 0]
    Comp_well  = [point[1] for point in sorted_points if point[0] != 0]
    return Comp_Volume, Comp_well

def break_list_element(temp,temp2):
    for j in range(len(temp)):
        if temp[j]>50:
            return [temp[0:j],temp[j:]], [temp2[0:j],temp2[j:]]
            break
    return [temp],[temp2]

for i in range(len(VOLUMES)):   # i represents components
	Comp_Volume_50,Comp_Volume_300,Comp_well_50,Comp_well_300=[],[],[],[]
	Comp = All_Component[i]

	for j in range(len(VOLUMES[i])):    # j represents labwares for those components

		Comp_Volume   = VOLUMES[i][j]
		Comp_well     =	WELLS[i][j]
		Comp_Volume,Comp_well = sort_volume_n_well(Comp_Volume,Comp_well)
		Comp_Volume,Comp_well = break_list_element(Comp_Volume,Comp_well)

		#Assigning Comp_well_50 and Comp_well_300 to the tuberacks
		if len(Comp_Volume)==1:
			Comp_Volume_50.append(Comp_Volume[0])
			Comp_well_50.append(Comp_well[0])
		else:
			Comp_Volume_50.append(Comp_Volume[0])
			Comp_Volume_300.append(Comp_Volume[1])
			Comp_well_50.append(Comp_well[0])
			Comp_well_300.append(Comp_well[1])


	# p50.set_pick_up_current(0.45)
	counter=0
	p50.pick_up_tip()
	for j in range(len(Comp_Volume_50)):    # j represents labwares for those components
# Using the P50 for all tuberacks
# Here we needed to use two separate transfer commands because in the transfer command if your destination
# well is just one well then you can use the ".top(-2)" in the transfer command itself. BUT, if the destination
# well is a list of wells then you cannot use ".top(-2)" in the transfefr command, you need to define a separate list
# that contains those same wells but has the information of ".top(-2)".
# this is why we are using well50 and well300. If any of the destination sublist has one element then we will not need
# well50 list in the transfer command.

		well50 = [wells.top(-2) for wells in tube_rack[j].wells(Comp_well_50[j])]
		if Comp_well_50[j]:

			if len(Comp_well_50[j])!=1:
				p50.transfer(
						Comp_Volume_50[j],
						Comp.top(-16),							# Change the Negative value if you need to aspirate deeper
						well50,
						blow_out=True,
						#touch_tip=True,
						new_tip='never')
			else:
				p50.transfer(
						Comp_Volume_50[j],
						Comp.top(-16),							# Change the Negative value if you need to aspirate deeper
						tube_rack[j].wells(Comp_well_50[j]).top(-2),
						blow_out=True,
						#touch_tip=True,
						new_tip='never')

	for i in Comp_Volume_50:
		if not i:
			counter=counter+1
	if counter==len(Comp_Volume_50):
		p50.return_tip()
	else:
		p50.drop_tip()


	# p300.set_pick_up_current(0.45)
	counter=0
	p300.pick_up_tip()
	for j in range(len(Comp_Volume_300)):    # j represents labwares for those components
	    # Using the P300 for all tuberacks
		well300 = [wells.top(-2) for wells in tube_rack[j].wells(Comp_well_300[j])]
		if Comp_well_300[j]:

			if len(Comp_well_300[j])!=1:
				p300.transfer(
						Comp_Volume_300[j],
						Comp.top(-15),						# Change the Negative value if you need to aspirate deeper
						well300,
						blow_out=True,
						# touch_tip=True,
						new_tip='never')
			else:
				p300.transfer(
							Comp_Volume_300[j],
							Comp.top(-15),					# Change the Negative value if you need to aspirate deeper
							tube_rack[i].wells(Comp_well_300[j]).top(-2),
							blow_out=True,
							# touch_tip=True,
							new_tip='never')
	for i in Comp_Volume_300:
		if not i:
			counter=counter+1
	if counter==len(Comp_Volume_300):
		p300.return_tip()
	else:
		p300.drop_tip()
