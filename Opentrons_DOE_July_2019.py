"""
@author DHull
@date July, 2019
"""

import numpy as np
import math, time, csv, os, signal
from opentrons import labware, instruments, robot, containers

def setup():
	global header, p50, p300, stock_wells, tube_rack, df
	df = np.genfromtxt('solutionmaker.csv', delimiter=',',skip_header=1, missing_values='')
	with open('solutionmaker.csv') as csvfile:
		reader_object = csv.reader(csvfile)
		header = [row for i_row, row in enumerate(reader_object) if i_row==0]

	(nrows, ncols) = df.shape
	for n_row in range(nrows):
		if (df[n_row,:].sum() > 1500):
			raise ValueError('Individual wells will not tolerate addition of this much volume')

	"""
	The following are constants for instantiation (mm/sec or ul/sec)
	-----------------------------------------
	"""
	XSPEED = 600
	YSPEED = 600
	ZSPEED = 125
	P300_ASPIRATERATE = 150
	P50_ASPIRATE = 25
	P50_DISPENSERATE = 100
	P300_DISPENSERATE = 600
	"""
	------------------------------------------
	"""

	# connects robot and sets robot settings
	robot.home()
	robot.connect()
	robot.head_speed(x=XSPEED, y=YSPEED, z=ZSPEED)

	# sets up labware and the layout of the experiment
	m300rack_1 = containers.load('tiprack-200ul', '10', share='True')
	m300rack_2 = containers.load('tiprack-200ul', '11', share='True')
	stock_wells=[]
	slot_plate_wells = ['4', '5']
	for slot in slot_plate_wells:
		stock_wells.append(containers.load('plate_6_well', slot, share='True'))
	stock_wells.append(containers.load('96-flat','6', share='True'))
	tube_rack =[]
	slots_tube_rack = ['1','2','3']
	for slot in slots_tube_rack:
		tube_rack.append(containers.load('4x6_Tube_rack', slot, share='True'))

	# instantiates pipettes
	p50 = instruments.P50_Single(mount="right",tip_racks=[m300rack_1], aspirate_flow_rate= P50_ASPIRATE, dispense_flow_rate= P50_DISPENSERATE)
	p300 = instruments.P300_Single(mount="left",tip_racks=[m300rack_2], aspirate_flow_rate= P300_ASPIRATERATE,dispense_flow_rate=P300_DISPENSERATE)

def func():
	global stock_index, aliquot_index, p50, p300, tube_rack, stock_wells, df, flag
	robot.home()
	"""
	The following are constants for transfering volumes
	-----------------------------------------
	"""
	TOUCH_RADIUS = 2.0
	TOUCH_SPEED = 20.0 # slowest it can go
	BOTTOM_OFFSET_ASPIRATE = 1 # mm
	TOP_OFFSET_DISPENSE = -10 # mm
	PAUSE_BLOWOUT = 1.0 # seconds
	flag = 0
	TOUCH_TIP_HEIGHT = -10.0
	"""
	------------------------------------------
	"""
	for stock_index, component in enumerate(header[0]):
		for aliquot_index, volume in enumerate(df[:, stock_index]):
			if volume != 0:
				print('Going to collect from well: ' + str(stock_index + 1))
				print('Going to dispense ' + str(volume) + ' to well: ' + str(aliquot_index + 1))
			temp_flag = flag
			aliquot_rem = aliquot_index % 24
			aliquot_quot = math.floor(aliquot_index / 24)
			# handles the 96 well plate in slot 6
			if stock_index < 12:
				stock_rem = stock_index % 6
				stock_quot = math.floor(stock_index / 6)
			else:
				stock_quot = 2
				stock_rem = stock_index-12
			if volume == 0.0:
				pass
			elif volume <= 50:
				p50.pick_up_tip()
				p50.aspirate(volume, stock_wells[stock_quot].wells(stock_rem).bottom(BOTTOM_OFFSET_ASPIRATE))
				p50.dispense(volume, tube_rack[aliquot_quot].wells(aliquot_rem).top(TOP_OFFSET_DISPENSE))
				time.sleep(PAUSE_BLOWOUT)
				p50.blow_out()
				time.sleep(PAUSE_BLOWOUT)
				p50.blow_out()
				p50.touch_tip(radius=TOUCH_RADIUS, speed=TOUCH_SPEED, v_offset=TOUCH_TIP_HEIGHT)
				p50.drop_tip()
			elif 50 < volume <= 300:
				p300.pick_up_tip()
				p300.aspirate(volume, stock_wells[stock_quot].wells(stock_rem).bottom(BOTTOM_OFFSET_ASPIRATE))
				p300.dispense(volume, tube_rack[aliquot_quot].wells(aliquot_rem).top(TOP_OFFSET_DISPENSE))
				time.sleep(PAUSE_BLOWOUT)
				p300.blow_out()
				time.sleep(PAUSE_BLOWOUT)
				p300.blow_out()
				p300.touch_tip(radius=TOUCH_RADIUS, speed=TOUCH_SPEED, v_offset=TOUCH_TIP_HEIGHT)
				p300.drop_tip()
			elif volume > 300:
				p300.pick_up_tip()
				quotient = math.floor(volume / 300)
				remainder = volume % 300
				for i in range(quotient):
					p300.aspirate(300, stock_wells[stock_quot].wells(stock_rem).bottom(BOTTOM_OFFSET_ASPIRATE))
					p300.dispense(300, tube_rack[aliquot_quot].wells(aliquot_rem).top(TOP_OFFSET_DISPENSE))
					time.sleep(PAUSE_BLOWOUT)
					p300.blow_out()
					time.sleep(PAUSE_BLOWOUT)
					p300.blow_out()
					p300.touch_tip(radius=TOUCH_RADIUS, speed=TOUCH_SPEED, v_offset=TOUCH_TIP_HEIGHT)
				if remainder <= 50:
					p50.pick_up_tip()
					p50.aspirate(remainder, stock_wells[stock_quot].wells(stock_rem).bottom(BOTTOM_OFFSET_ASPIRATE))
					p50.dispense(remainder, tube_rack[aliquot_quot].wells(aliquot_rem).top(TOP_OFFSET_DISPENSE))
					time.sleep(PAUSE_BLOWOUT)
					p50.blow_out()
					p50.blow_out()
					p50.touch_tip(radius=TOUCH_RADIUS, speed=TOUCH_SPEED, v_offset=TOUCH_TIP_HEIGHT)
					p50.drop_tip()
				else:
					p300.aspirate(remainder, stock_wells[stock_quot].wells(stock_rem).bottom(BOTTOM_OFFSET_ASPIRATE))
					p300.dispense(remainder, tube_rack[aliquot_quot].wells(aliquot_rem).top(TOP_OFFSET_DISPENSE))
					time.sleep(PAUSE_BLOWOUT)
					p300.blow_out()
					time.sleep(PAUSE_BLOWOUT)
					p300.blow_out()
					p300.touch_tip(radius=TOUCH_RADIUS, speed=TOUCH_SPEED, v_offset=TOUCH_TIP_HEIGHT)
					p300.drop_tip()
			else:
				pass
			if temp_flag!=flag:
				input('Press Enter To Continue')

def keyboardInterruptHandler(signal, frame):
	global flag
	flag+=1

setup()
signal.signal(signal.SIGINT, keyboardInterruptHandler)
func()
