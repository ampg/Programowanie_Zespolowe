"""
CarSetup v2.65
by David Ludwig
http://www.youtube.com/blender3dmaster
"""

#import blender game engine content
from bge import logic, constraints
#import other modules
import math, mathutils
import time


class CarSetup:
	maxRPM = 4.15
	minRPM = 0
	nRPM = 0.4
	RPM = 0
	autoRPM = 2
	
	MaxSpeed_RG = 0.4
	MaxSpeed_1G = 1.1
	MaxSpeed_2G = 2.2
	
	MaxSpeed_3G = 3.2
	MinSpeed_3G = 0.4
	
	MaxSpeed_4G = 3.9
	MinSpeed_4G = 0.5
	
	MaxSpeed_5G = 4.9
	MinSpeed_5G = 0.6
	
	MinSpeed = 0
	Speed = 0
	
	
	
	w = 0
	wON = False
	wMax = 2.0
	wMin = 0
	wUp = False
	
	def __init__(self):

		#list of cars
		self.carList = {}
		
		#list of tires
		self.tires = {}
		
		#car turn amount
		self.turnAmount = {}
	def carInitialized(self, car):
		
		#check for initialized property
		if "initialized" in car:
			
			#check if car is initialized
			if car["initialized"] == True:
				
				#car is initialized
				return True
		
		#car is not initialized
		return False
	def carConstraint(self, car):
		
		#get physics ID
		carPhysicsID = car.getPhysicsId()
		 
		#create a vehicle constraint 
		vehicleConstraint = constraints.createConstraint(carPhysicsID, 0, 11)
		 
		#get the constraint ID
		constraintID = vehicleConstraint.getConstraintId()
		  
		#get the vehicle constraint ID
		vehicleID =  constraints.getVehicleConstraint(constraintID)
	
		#save vehicle constraint ID as an object variable
		car["vehicleID"] = vehicleID
		
		#return vehicle ID
		return vehicleID
	def positionTires(self, car):
		
		#get the list of tires
		tireList = self.tires[car]
		
		tire1 = tireList["TireFD"]	#tire front drivers
		tire2 = tireList["TireFP"]	#tire front passengers
		tire3 = tireList["TireRD"]	#tire rear drivers
		tire4 = tireList["TireRP"]	#tire rear passnengers
		
		tire1Pos = tire1.worldPosition	#tire front drivers
		tire2Pos = tire2.worldPosition	#tire front passengers
		tire3Pos = tire3.worldPosition	#tire rear drivers
		tire4Pos = tire4.worldPosition	#tire rear passnengers
		
		#car position
		carPos = car.worldPosition
		
		#tire front drivers
		tire1Pos = [tire1Pos[0] - carPos[0],
					tire1Pos[1] - carPos[1],
					tire1Pos[2] - carPos[2]]
		
		#tire front passengers
		tire2Pos = [tire2Pos[0] - carPos[0],
					tire2Pos[1] - carPos[1],
					tire2Pos[2] - carPos[2]]
		
		#tire rear drivers
		tire3Pos = [tire3Pos[0] - carPos[0],
					tire3Pos[1] - carPos[1],
					tire3Pos[2] - carPos[2]]
		
		#tire rear passengers
		tire4Pos = [tire4Pos[0] - carPos[0],
					tire4Pos[1] - carPos[1],
					tire4Pos[2] - carPos[2]]
			
		return (tire1Pos, tire2Pos, tire3Pos, tire4Pos)
	def tireRadius(self, car):
		
		#get the list of tires
		tireList = self.tires[car]
		
		tire1Radius = tireList["TireFD"].localScale[2]/2	#tire front drivers
		tire2Radius = tireList["TireFP"].localScale[2]/2	#tire front passengers
		tire3Radius = tireList["TireRD"].localScale[2]/2	#tire rear drivers
		tire4Radius = tireList["TireRP"].localScale[2]/2	#tire rear passengers
		
		#check for radius override
		if "Radius" in tireList["TireFD"]:
			tire1Radius = tireList["TireFD"]["Radius"]
			
		if "Radius" in tireList["TireFP"]:
			tire2Radius = tireList["TireFP"]["Radius"]
			
		if "Radius" in tireList["TireRD"]:
			tire3Radius = tireList["TireRD"]["Radius"]
			
		if "Radius" in tireList["TireRP"]:
			tire4Radius = tireList["TireRP"]["Radius"]
		
		return (tire1Radius, tire2Radius, tire3Radius, tire4Radius)
	def suspensionHeight(self, car):
		
		tireList = self.tires[car]
		
		tire1height = 0.0	#tire front drivers
		tire2height = 0.0	#tire front passengers
		tire3height = 0.0	#tire rear drivers
		tire4height = 0.0	#tire rear passengers
		
		#check for suspension height override
		if "Height" in tireList["TireFD"]:
			tire1height = tireList["TireFD"]["Height"]
			
		if "Height" in tireList["TireFP"]:
			tire2height = tireList["TireFP"]["Height"]
			
		if "Height" in tireList["TireRD"]:
			tire3height = tireList["TireRD"]["Height"]
			
		if "Height" in tireList["TireRP"]:
			tire4height = tireList["TireRP"]["Height"]
		
		return (tire1height, tire2height, tire3height, tire4height)
	def suspensionAngle(self):
		
		tire1Angle = [0, 0, -1]	#tire front drivers
		tire2Angle = [0, 0, -1]	#tire front passengers
		tire3Angle = [0, 0, -1]	#tire rear drivers
		tire4Angle = [0, 0, -1]	#tire rear passengers
		
		return (tire1Angle, tire2Angle, tire3Angle, tire4Angle)
	def tireAxis(self):
		
		tire1Axis = [-1, 0, 0]	#tire front drivers
		tire2Axis = [-1, 0, 0]	#tire front passengers
		tire3Axis = [-1, 0, 0]	#tire rear drivers
		tire4Axis = [-1, 0, 0]	#tire rear passengers
		
		return (tire1Axis, tire2Axis, tire3Axis, tire4Axis)
	def tireSteering(self):
		
		tire1Steer = True	#tire front drivers
		tire2Steer = True	#tire front passengers
		tire3Steer = False	#tire rear drivers
		tire4Steer = False	#tire rear passengers
		
		return (tire1Steer, tire2Steer, tire3Steer, tire4Steer)
	def addTires(self, car, vehicleID):
		
		#get the list of tires
		tireList = self.tires[car]
		
		#list the tires
		tires = [tireList["TireFD"],
				 tireList["TireFP"],
				 tireList["TireRD"],
				 tireList["TireRP"]]
		
		#position the tires
		tirePos = self.positionTires(car)
		
		#calculate tire radius
		tireRadius = self.tireRadius(car)
		
		#get the suspension heght
		suspensionHeight = self.suspensionHeight(car)
		
		#get the suspension angle
		suspensionAngle = self.suspensionAngle()
		
		#get the tire axis
		tireAxis = self.tireAxis()
		
		#get which wheels turn
		tireSteer = self.tireSteering()
		
		for tire in range(0, 4):
			
			#tire object
			obj = tires[tire]
			
			#tire position
			pos = tirePos[tire]
			
			#tire suspension height
			suspenHeight = suspensionHeight[tire]
			
			#angle of suspension
			suspenAngle = suspensionAngle[tire]
			
			#tire rotation axis
			axis = tireAxis[tire]
			
			#tire radius
			radius = tireRadius[tire]
			
			#tire steering
			steering = tireSteer[tire]
			
			#add wheel to car
			vehicleID.addWheel(obj, pos, suspenAngle, axis, suspenHeight, radius, steering)
	def tireGrip(self, car, vehicleID):
		
		#list of tires
		tireList = self.tires[car]
		
		tire1Grip = 10	#tire front drivers
		tire2Grip = 10	#tire front Passengers
		tire3Grip = 10	#tire rear drivers
		tire4Grip = 10	#tire rear passengers
		
		#check for grip override
		if "Grip" in tireList["TireFD"]:
			tire1Grip = tireList["TireFD"]["Grip"]
			
		if "Grip" in tireList["TireFP"]:
			tire2Grip = tireList["TireFP"]["Grip"]
			
		if "Grip" in tireList["TireRD"]:
			tire3Grip = tireList["TireRD"]["Grip"]
			
		if "Grip" in tireList["TireRP"]:
			tire4Grip = tireList["TireRP"]["Grip"]
		
		vehicleID.setTyreFriction(tire1Grip, 0)	#tire front drivers
		vehicleID.setTyreFriction(tire2Grip, 1)	#tire front Passengers
		vehicleID.setTyreFriction(tire3Grip, 2)	#tire rear drivers
		vehicleID.setTyreFriction(tire4Grip, 3)	#tire rear passengers
	def suspensionCompression(self, car, vehicleID):
		
		#list of tires
		tireList = self.tires[car]
		
		tire1Compress = 6	#tire front drivers
		tire2Compress = 6	#tire front Passengers
		tire3Compress = 6	#tire rear drivers
		tire4Compress = 6	#tire rear passengers
		
		#check for compression override
		if "Compression" in tireList["TireFD"]:
			tire1Compress = tireList["TireFD"]["Compression"]
			
		if "Compression" in tireList["TireFP"]:
			tire2Compress = tireList["TireFP"]["Compression"]
			
		if "Compression" in tireList["TireRD"]:
			tire3Compress = tireList["TireRD"]["Compression"]
			
		if "Compression" in tireList["TireRP"]:
			tire4Compress = tireList["TireRP"]["Compression"]
		
		vehicleID.setSuspensionCompression(tire1Compress, 0)	#tire front drivers
		vehicleID.setSuspensionCompression(tire2Compress, 1)	#tire front Passengers
		vehicleID.setSuspensionCompression(tire3Compress, 2)	#tire rear drivers
		vehicleID.setSuspensionCompression(tire4Compress, 3)	#tire rear passengers
	def suspensionDamping(self, car, vehicleID):
		
		#list of tires
		tireList = self.tires[car]
		
		tire1Damp = 5	#tire front drivers
		tire2Damp = 5	#tire front Passengers
		tire3Damp = 5	#tire rear drivers
		tire4Damp = 5	#tire rear passengers
		
		#check for damping override
		if "Damping" in tireList["TireFD"]:
			tire1Damp = tireList["TireFD"]["Damping"]
			
		if "Damping" in tireList["TireFP"]:
			tire2Damp = tireList["TireFP"]["Damping"]
			
		if "Damping" in tireList["TireRD"]:
			tire3Damp = tireList["TireRD"]["Damping"]
			
		if "Damping" in tireList["TireRP"]:
			tire4Damp = tireList["TireRP"]["Damping"]
		
		vehicleID.setSuspensionDamping(tire1Damp, 0)	#tire front drivers
		vehicleID.setSuspensionDamping(tire2Damp, 1)	#tire front Passengers
		vehicleID.setSuspensionDamping(tire3Damp, 2)	#tire rear drivers
		vehicleID.setSuspensionDamping(tire4Damp, 3)	#tire rear passengers
	def suspensionStiffness(self, car, vehicleID):
		
		#list of tires
		tireList = self.tires[car]
		
		tire1Stiffness = 12.5		#tire front drivers
		tire2Stiffness = 12.5		#tire front Passengers
		tire3Stiffness = 12.5		#tire rear drivers
		tire4Stiffness = 12.5		#tire rear passengers
		
		#check for stiffness override
		if "Stiffness" in tireList["TireFD"]:
			tire1Stiffness = tireList["TireFD"]["Stiffness"]
			
		if "Stiffness" in tireList["TireFP"]:
			tire2Stiffness = tireList["TireFP"]["Stiffness"]
			
		if "Stiffness" in tireList["TireRD"]:
			tire3Stiffness = tireList["TireRD"]["Stiffness"]
			
		if "Stiffness" in tireList["TireRP"]:
			tire4Stiffness = tireList["TireRP"]["Stiffness"]
		
		vehicleID.setSuspensionStiffness(tire1Stiffness, 0)	#tire front drivers
		vehicleID.setSuspensionStiffness(tire2Stiffness, 1)	#tire front Passengers
		vehicleID.setSuspensionStiffness(tire3Stiffness, 2)	#tire rear drivers
		vehicleID.setSuspensionStiffness(tire4Stiffness, 3)	#tire rear passengers
	def suspensionRollInfluence(self, car, vehicleID):
		
		#list of tires
		tireList = self.tires[car]
		
		tire1Roll = -0.016	#tire front drivers
		tire2Roll = -0.016	#tire front Passengers
		tire3Roll = -0.016	#tire rear drivers
		tire4Roll = -0.016	#tire rear passengers
		
		#check for roll influence override
		if "RollInfluence" in tireList["TireFD"]:
			tire1Roll = -tireList["TireFD"]["RollInfluence"]
			
		if "Roll" in tireList["TireFP"]:
			tire2Roll = -tireList["TireFP"]["RollInfluence"]
			
		if "Roll" in tireList["TireRD"]:
			tire3Roll = -tireList["TireRD"]["RollInfluence"]
			
		if "Roll" in tireList["TireRP"]:
			tire4Roll = -tireList["TireRP"]["RollInfluence"]
		
		vehicleID.setRollInfluence(tire1Roll, 0)	#tire front drivers
		vehicleID.setRollInfluence(tire2Roll, 1)	#tire front Passengers
		vehicleID.setRollInfluence(tire3Roll, 2)	#tire rear drivers
		vehicleID.setRollInfluence(tire4Roll, 3)	#tire rear passengers

	
#create CarSetup object
carsetup = CarSetup()
def _initialize(controller):
	
	#get the car object
	car = controller.owner
	
	#get current orientation
	carOrient = car.worldOrientation
	
	#convert orientation to euler
	carEuler = carOrient.to_euler()
	newCarEuler = carOrient.to_euler()
	
	#set euler rotation
	newCarEuler[0] = 0
	newCarEuler[1] = 0
	newCarEuler[2] = 0
	
	#set car orientation
	car.worldOrientation = newCarEuler.to_matrix()
	
	if not car.name in carsetup.carList:
		
		#assign the car
		carsetup.carList[car] = car
		
		tires = {}
		
		#look for tires
		for c in car.children:
			
			tire = "Tire"
			
			#check if tire object
			if "Tire" in c:
				
				#build the tire name
				tire += c["Tire"]
				
				#add tire to list
				tires[tire] = c
				
				#assign tires owner
				c["owner"] = car.name
				
				#clear tire parent
				c.removeParent()
		
		#add tires to list of tires
		carsetup.tires[car] = tires
		
		#build the car constraint
		vehicleID = carsetup.carConstraint(car)
		
		#add tires to car
		carsetup.addTires(car, vehicleID)
		
		#set tire grip
		carsetup.tireGrip(car, vehicleID)
		
		#set suspension compression
		carsetup.suspensionCompression(car, vehicleID)
		
		#set suspension damping
		carsetup.suspensionDamping(car, vehicleID)
		
		#set suspension stiffness
		carsetup.suspensionStiffness(car, vehicleID)
		
		#set suspension roll influence
		carsetup.suspensionRollInfluence(car, vehicleID)
	
	#set car orientation
	car.worldOrientation = carEuler.to_matrix()
	
	#set car to initialized
	car["initialized"] = True
	
	#set turn amount
	carsetup.turnAmount[car] = 0
	
	#check for "TurnAmount" property in car
	if not "TurnAmount" in car:
		
		#set default turn amount
		car["TurnAmount"] = 25
		
	#check for "TurnSpeed" property in car
	if not "TurnSpeed" in car:
		
		#set default turn speed
		car["TurnSpeed"] = 5
def _constraintID(car):
		
	# get saved vehicle Constraint ID
	vehicleID = car["vehicleID"]
	
	return vehicleID
def _powertrain(controller, car):

	#declare variables
	gas = None
	#moje
	gearUp = None
	gearDown = None
	scene = logic.getCurrentScene()
	StreetLamp = scene.objects["StreetLamp"]
	SpeedMeter = scene.objects["SpeedMeter"]
	#/moje
	reverse = None
	brake = None
	ebrake = None
	
	#get the vehicl id
	vehicleID = _constraintID(car)
	
	#engine power
	power = 0
	
	#engine
	engine = False
	
	#check for engine override
	if "Engine" in car:
		engine = car["Engine"]
	
	#set default values
	forwardSpeed = 100
	#moje
	currentGear = 0
	#/moje
	reverseSpeed = 300
	brakeAmount = 65
	eBrakeAmount = 100
	backdrive = False
	frontdrive = True

	#check for forward speed override
	if "ForwardSpeed" in car:
		
		#set forward speed
		forwardSpeed = car["ForwardSpeed"]

	#moje
	if "CurrentGear" in car:
		currentGear = car["CurrentGear"]
	#/moje
	
	#check for reverse speed override
	if "ReverseSpeed" in car:
		
		#set reverse speed
		reverseSpeed = car["ReverseSpeed"]
	
	#check for brake amount override
	if "BrakeAmount" in car:
		
		#set brake amount
		brakeAmount = car["BrakeAmount"]
	
	#check for E-brake amount override
	if "EBrakeAmount" in car:
		
		#set brake amount
		eBrakeAmount = car["EBrakeAmount"]
	
	#check for BackWheelDrive override
	if "BackWheelDrive" in car:
		
		#set back wheel drive
		backdrive = car["BackWheelDrive"]
	
	#check for FrontWheelDrive override
	if "FrontWheelDrive" in car:
		
		#set front wheel drive
		frontdrive = car["FrontWheelDrive"]
	
	#check for gas sensor
	if "Gas" in controller.sensors:
		gas = controller.sensors["Gas"]
	
	#check for reverse sensor
	if "Reverse" in controller.sensors:
		reverse = controller.sensors["Reverse"]
	
	#check for brake sensor
	if "Brake" in controller.sensors:
		brake = controller.sensors["Brake"]
	
	#check for E-brake sensor
	if "EBrake" in controller.sensors:
		ebrake = controller.sensors["EBrake"]

	#moje
	if "GearUp" in controller.sensors:
		gearUp = controller.sensors["GearUp"]

	if "GearDown" in controller.sensors:
		gearDown = controller.sensors["GearDown"]

	if "StartStop" in controller.sensors:
		startStop = controller.sensors["StartStop"]
	#/moje

	#check if gas exists
	if gas:
		#check if engine is on
		if engine:
			#check if gas is positive
			if gas.positive:
				#print("funkcja gas")
				#set power
				if currentGear == -1:
					forwardSpeed = -1000
					if carsetup.RPM < carsetup.maxRPM:
						carsetup.RPM += 0.00001 + (carsetup.RPM/100)
						StreetLamp.applyRotation([0, 0.00001 + (carsetup.RPM/100), 0], 1)
						#if carsetup.Speed <= carsetup.MaxSpeed_1G:
						SpeedMeter.applyRotation([0, 0.005,0],1)
						carsetup.Speed += 0.005
						forwardSpeed = (carsetup.Speed*50)*(carsetup.RPM+50)
						power = forwardSpeed
						
				elif currentGear == 0:
					forwardSpeed = 0
					if carsetup.RPM <= carsetup.maxRPM:
						StreetLamp.applyRotation([0, 0.1, 0], 1)
						carsetup.RPM += 0.1
					if carsetup.Speed > carsetup.MinSpeed:
						SpeedMeter.applyRotation([0, -0.005, 0], 1)
						carsetup.Speed -= 0.005
						
				elif currentGear == 1:
					if carsetup.RPM < carsetup.autoRPM:
						carsetup.RPM += 0.00001 + (carsetup.RPM/100)
						StreetLamp.applyRotation([0, 0.00001 + (carsetup.RPM/100), 0], 1)
						SpeedMeter.applyRotation([0, (carsetup.Speed+0.1)/(carsetup.maxRPM - carsetup.RPM)*0.035,0],1)
						carsetup.Speed += (carsetup.Speed+0.1)/(carsetup.maxRPM - carsetup.RPM)*0.035
						forwardSpeed = (carsetup.Speed*100)*(carsetup.RPM+150)
						power = -forwardSpeed
					else:
						car["CurrentGear"] = currentGear + 1
						StreetLamp.applyRotation([0, -1, 0], 1)
						carsetup.RPM -= 1
						
				elif currentGear == 2:
					if carsetup.RPM < carsetup.autoRPM:
						carsetup.RPM += 0.00001 + (carsetup.RPM/200)
						StreetLamp.applyRotation([0, 0.00001 + (carsetup.RPM/200) , 0], 1)
						forwardSpeed = 200
						power = -forwardSpeed
						SpeedMeter.applyRotation([0, (carsetup.Speed+0.1)/(carsetup.maxRPM - carsetup.RPM)*0.01,0],1)
						carsetup.Speed += (carsetup.Speed+0.1)/(carsetup.maxRPM - carsetup.RPM)*0.01
						forwardSpeed = (carsetup.Speed*10)*(carsetup.RPM+150)
						power = -forwardSpeed
					else:
						car["CurrentGear"] = currentGear + 1
						StreetLamp.applyRotation([0, -1, 0], 1)
						carsetup.RPM -= 1

				elif currentGear == 3:
					if carsetup.RPM < carsetup.autoRPM:
						carsetup.RPM += 0.00001 + (carsetup.RPM/300)
						StreetLamp.applyRotation([0, 0.00001 + (carsetup.RPM/300) , 0], 1)
						forwardSpeed = 200
						power = -forwardSpeed
						SpeedMeter.applyRotation([0, (carsetup.Speed+0.1)/(carsetup.maxRPM - carsetup.RPM)*0.005,0],1)
						carsetup.Speed += (carsetup.Speed+0.1)/(carsetup.maxRPM - carsetup.RPM)*0.005
						forwardSpeed = (carsetup.Speed*10)*(carsetup.RPM+150)
						power = -forwardSpeed
					else:
						car["CurrentGear"] = currentGear + 1
						StreetLamp.applyRotation([0, -1, 0], 1)
						carsetup.RPM -= 1
						
				elif currentGear == 4:
					if carsetup.RPM < carsetup.autoRPM:
						carsetup.RPM += 0.00001 + (carsetup.RPM/600)
						StreetLamp.applyRotation([0, 0.00001 + (carsetup.RPM/600) , 0], 1)
						forwardSpeed = 200
						power = -forwardSpeed
						SpeedMeter.applyRotation([0, (carsetup.Speed+0.1)/(carsetup.maxRPM - carsetup.RPM)*0.002,0],1)
						carsetup.Speed += (carsetup.Speed+0.1)/(carsetup.maxRPM - carsetup.RPM)*0.002
						forwardSpeed = (carsetup.Speed*10)*(carsetup.RPM+150)
						power = -forwardSpeed
					else:
						car["CurrentGear"] = currentGear + 1
						StreetLamp.applyRotation([0, -1, 0], 1)
						carsetup.RPM -= 1
						
				elif currentGear == 5:
					if carsetup.RPM <= carsetup.maxRPM:
						carsetup.RPM += 0.00001 + (carsetup.RPM/800)
						StreetLamp.applyRotation([0, 0.00001 + (carsetup.RPM/800) , 0], 1)
					if carsetup.Speed < carsetup.MaxSpeed_5G:
						SpeedMeter.applyRotation([0, (carsetup.Speed+0.1)/(carsetup.maxRPM - carsetup.RPM)*0.001,0],1)
						carsetup.Speed += (carsetup.Speed+0.1)/(carsetup.maxRPM - carsetup.RPM)*0.001
						forwardSpeed = (carsetup.Speed*10)*(carsetup.RPM+150)
						power = -forwardSpeed
						
			else:
				if currentGear == -1:
					if carsetup.Speed > carsetup.MinSpeed:
						SpeedMeter.applyRotation([0, -0.008 * (carsetup.Speed/(carsetup.RPM)), 0], 1)
						carsetup.Speed -= (0.008 * (carsetup.Speed/(carsetup.RPM)))
					if carsetup.RPM > carsetup.nRPM:
						StreetLamp.applyRotation([0, -0.008, 0], 1)
						carsetup.RPM -= 0.008
				if currentGear == 0:
					power = 0
					if carsetup.Speed > carsetup.MinSpeed:
						SpeedMeter.applyRotation([0, -0.003, 0], 1)
						carsetup.Speed -= 0.003
					if carsetup.RPM <= carsetup.nRPM:
						StreetLamp.applyRotation([0, 0.03, 0], 1)
						carsetup.RPM += 0.03
					elif carsetup.RPM > carsetup.nRPM:
						StreetLamp.applyRotation([0, -0.02, 0], 1)
						carsetup.RPM -= 0.02
				if currentGear == 1:
					if carsetup.Speed > carsetup.MinSpeed:
						SpeedMeter.applyRotation([0, -0.008 * (carsetup.Speed/(carsetup.RPM)), 0], 1)
						carsetup.Speed -= (0.008 * (carsetup.Speed/(carsetup.RPM)))
						forwardSpeed = (carsetup.Speed*10)*(carsetup.RPM+50)
						power = -forwardSpeed	
					if carsetup.RPM > carsetup.nRPM:
						StreetLamp.applyRotation([0, -0.008, 0], 1)
						carsetup.RPM -= 0.008
					if carsetup.Speed >= carsetup.MinSpeed:
						forwardSpeed = (carsetup.Speed*10)*(carsetup.RPM+50)
						power = -forwardSpeed								
				if currentGear == 2:
					if carsetup.Speed > carsetup.MinSpeed:
						SpeedMeter.applyRotation([0, -0.001 * (carsetup.Speed/(carsetup.RPM)), 0], 1)
						carsetup.Speed -= (0.001 * (carsetup.Speed/(carsetup.RPM)))
					if carsetup.RPM > carsetup.nRPM:
						StreetLamp.applyRotation([0, -0.003, 0], 1)
						carsetup.RPM -= 0.003
					else:
						car["CurrentGear"] = currentGear - 1
						StreetLamp.applyRotation([0, 1, 0], 1)
						carsetup.RPM += 1
				if currentGear == 3:
					if carsetup.Speed > carsetup.MinSpeed_3G:
						SpeedMeter.applyRotation([0, -0.001 * (carsetup.Speed/(carsetup.RPM)), 0], 1)
						carsetup.Speed -= (0.001 * (carsetup.Speed/(carsetup.RPM)))
					if carsetup.RPM > carsetup.nRPM:
						StreetLamp.applyRotation([0, -0.003, 0], 1)
						carsetup.RPM -= 0.003
					else:
						car["CurrentGear"] = currentGear - 1
						StreetLamp.applyRotation([0, 1, 0], 1)
						carsetup.RPM += 1
				if currentGear == 4:
					if carsetup.Speed > carsetup.MinSpeed_4G:
						SpeedMeter.applyRotation([0, -0.001 * (carsetup.Speed/(carsetup.RPM)), 0], 1)
						carsetup.Speed -= (0.001 * (carsetup.Speed/(carsetup.RPM)))
					if carsetup.RPM > carsetup.nRPM:
						StreetLamp.applyRotation([0, -0.003, 0], 1)
						carsetup.RPM -= 0.003
					else:
						car["CurrentGear"] = currentGear - 1
						StreetLamp.applyRotation([0, 1, 0], 1)
						carsetup.RPM += 1
				if currentGear == 5:
					if carsetup.Speed > carsetup.MinSpeed_5G:
						SpeedMeter.applyRotation([0, -0.001 * (carsetup.Speed/(carsetup.RPM)), 0], 1)
						carsetup.Speed -= (0.001 * (carsetup.Speed/(carsetup.RPM)))
					if carsetup.RPM > carsetup.nRPM:
						StreetLamp.applyRotation([0, -0.003, 0], 1)
						carsetup.RPM -= 0.003
					else:
						car["CurrentGear"] = currentGear - 1
						StreetLamp.applyRotation([0, 1, 0], 1)
						carsetup.RPM += 1
		elif not engine:
			if carsetup.RPM > carsetup.minRPM:
				StreetLamp.applyRotation([0, -0.05, 0], 1)
				carsetup.RPM -= 0.05
			if carsetup.Speed > carsetup.MinSpeed:
				SpeedMeter.applyRotation([0, -0.005, 0], 1)
				carsetup.Speed -= 0.005

	#moje
	if gearUp:
		if gearUp.positive:
			if currentGear == 0:
				if carsetup.RPM < 0.5 and carsetup.Speed < 0.1:
						power = 0
						car["CurrentGear"] = currentGear + 1
				else:
					print("Autmonatyczna skrzynia biegów zniszczona")
			if currentGear == -1:
				power = 0
				car["CurrentGear"] = currentGear + 1
	if gearDown:
		if gearDown.positive:
			if engine:
				if currentGear == 0:
					if carsetup.RPM < 0.5 and carsetup.Speed < 0.1:
						power = 0
						car["CurrentGear"] = currentGear - 1
					else:
						print("Autmonatyczna skrzynia biegów zniszczona")
				if currentGear == 1:
					power = 0
					car["CurrentGear"] = currentGear - 1
			else:
				if currentGear == 5:
					car["CurrentGear"] = currentGear - 1
				elif currentGear == 4:
					car["CurrentGear"] = currentGear - 1
				elif currentGear == 3:
					car["CurrentGear"] = currentGear - 1
				elif currentGear == 2:
					car["CurrentGear"] = currentGear - 1
				elif currentGear == 1:
					car["CurrentGear"] = currentGear - 1
				elif currentGear == 0:
					car["CurrentGear"] = currentGear - 1
	if startStop:
		if startStop.positive:
			if not engine and currentGear == 0:
				car["Engine"] = True
			elif engine  and carsetup.RPM < 0.5:
				car["Engine"] = False
	#/moje

	#check if reverse exists
	if reverse:
		
		#check if reverse is positive
		if reverse.positive:
			
			#check if engine is on
			if engine:
				
				#set power
				power = reverseSpeed
				
				#check if gas exists
				if gas:
					
					#check if gas is positive
					if gas.positive:
						
						#set power
						power = 0
	
	#check if brake exists
	if brake:
		
		#check if brake is positive
		if brake.positive:
			#moje
			#gas.negative
			#/moje
			#apply braking
			
			#moje
			if carsetup.Speed > carsetup.MinSpeed:
				SpeedMeter.applyRotation([0, -0.01 * (carsetup.Speed/(carsetup.RPM)), 0], 1)
				carsetup.Speed -= (0.01 * (carsetup.Speed/(carsetup.RPM)))
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.00001), 2)
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.00001), 3)
				power = 0
			if carsetup.RPM > carsetup.nRPM:
				StreetLamp.applyRotation([0, -0.012, 0], 1)
				carsetup.RPM -= 0.012
				
			#elif carsetup.RPM = carsetup.nRPM:
				#car["Engine"] = False
			#/moje
			
			#vehicleID.applyBraking(brakeAmount, 0)
			#vehicleID.applyBraking(brakeAmount, 1)
			#vehicleID.applyBraking(brakeAmount, 2)
			#vehicleID.applyBraking(brakeAmount, 3)
			
			#set power
			#power = 0

			#moje
			'''if carsetup.RPM > carsetup.minRPM and currentGear != 0:
				StreetLamp.applyRotation([0, -0.065, 0], 1)
				carsetup.RPM -= 0.065'''
			#elif carsetup.RPM = carsetup.nRPM:
				#car["Engine"] = False
			#/moje
			
		else:
			#remove braking
			vehicleID.applyBraking(0, 2)
			vehicleID.applyBraking(0, 3)
		
	#check if e brake exists
	if ebrake:
		
		#check if e brake is positive
		if ebrake.positive:
			
			#apply braking
			vehicleID.applyBraking(eBrakeAmount, 2)
			vehicleID.applyBraking(eBrakeAmount, 3)
			
			#set power
			power = 0
	
			
	#check if back wheel drive
	if backdrive:
		
		#apply power
		vehicleID.applyEngineForce(power, 2)
		vehicleID.applyEngineForce(power, 3)
		
	#check if front wheel drive
	if frontdrive:
		
		#apply power
		vehicleID.applyEngineForce(power, 0)
		vehicleID.applyEngineForce(power, 1)


#kiera = bge.logic.joysticks[0]
def _steer(controller, car):
	
	#moje
	scene = logic.getCurrentScene()
	StrWheel = scene.objects["SteeringWheel"]
	#av = kiera.axisValues
	#print("kiera")
	#print(kiera)
	#/moje

	#declare variables
	left = None
	right = None
	#turn amount
	#turnAmount = math.radians(car["TurnAmount"])
	
	#get turn speed
	turnSpeed = car["TurnSpeed"] * 0.005
	
	#get vehicle id
	vehicleID = _constraintID(car)

	#check for left sensor
	if "Left" in controller.sensors:
		left = controller.sensors["Left"]
		
	#check for right sensor
	if "Right" in controller.sensors:
		right = controller.sensors["Right"]
	#turnAmount = math.radians(right.axisValues[0])/800
	turnAmount = ((abs(right.axisValues[0]))/50000)
	#print(turnAmount)
	print(carsetup.turnAmount[car])
	
	#check if the sensors exist
	if left and right:
		
		#check if both are positive
		if left.positive and right.positive:
			pass

		#check if left is positive
		elif left.positive and not right.positive:
			#check turn amount
			if carsetup.turnAmount[car] < turnAmount:
				
				#add to turn value
				carsetup.turnAmount[car] += turnSpeed
				
				#apply steering
				vehicleID.setSteeringValue(carsetup.turnAmount[car],0)
				vehicleID.setSteeringValue(carsetup.turnAmount[car],1)

				#moje
				StrWheel.applyRotation([0, -0.1, 0], 1)
				#/moje
			#print("left")
		
		#check if right is positive
		elif not left.positive and right.positive:
			#check turn amount
			if carsetup.turnAmount[car] > -turnAmount:
				
				#subtract from turn value
				carsetup.turnAmount[car] -= turnSpeed
				
				#apply steering
				vehicleID.setSteeringValue(carsetup.turnAmount[car],0)
				vehicleID.setSteeringValue(carsetup.turnAmount[car],1)

				#moje
				StrWheel.applyRotation([0, 0.1, 0], 1)
				#/moje
			#print("right")
				
		#check if none are positive
		elif not left.positive and not right.positive:
			
			#check if steering right
			if carsetup.turnAmount[car] <= -turnSpeed:
				
				#add to turn value
				carsetup.turnAmount[car] += turnSpeed
				#moje
				StrWheel.applyRotation([0, -0.1, 0], 1)
				#/moje
				
			#check if steering left
			elif carsetup.turnAmount[car] > turnSpeed:
				
				#subtract from turn value
				carsetup.turnAmount[car] -= turnSpeed
				#moje
				StrWheel.applyRotation([0, 0.1, 0], 1)
				#/moje
			#print("not left not right")

				
			#apply steering
			vehicleID.setSteeringValue(carsetup.turnAmount[car], 0)
			vehicleID.setSteeringValue(carsetup.turnAmount[car], 1)
def _whipers(controller, car):
    scene = logic.getCurrentScene()
    whiper1 = scene.objects["whiper1"]
    whiper2 = scene.objects["whiper2"]
 
    whipersON = None
    if "WhipersON" in controller.sensors:
        whipersON = controller.sensors["WhipersON"]
    if whipersON:
        if whipersON.positive:
            if carsetup.wON == True:
                carsetup.wON = False
            elif carsetup.wON == False:
                carsetup.wON = True
        else:
            if carsetup.wON == True:
                if carsetup.wUp == True:
                    if carsetup.w <= carsetup.wMax:
                        whiper1.applyRotation([0, -0.05, 0], 1)
                        whiper2.applyRotation([0, -0.05, 0], 1)
                        carsetup.w += 0.05
                    else:
                        carsetup.wUp = False
                elif carsetup.wUp == False:
                    if carsetup.w >= carsetup.wMin:
                        whiper1.applyRotation([0, 0.05, 0], 1)
                        whiper2.applyRotation([0, 0.05, 0], 1)
                        carsetup.w -= 0.05
                    else:
                        carsetup.wUp = True
            elif carsetup.wON == False:
                if carsetup.wUp == True:
                    if carsetup.w <= carsetup.wMax:
                        whiper1.applyRotation([0, -0.05, 0], 1)
                        whiper2.applyRotation([0, -0.05, 0], 1)
                        carsetup.w += 0.05
                    else:
                        carsetup.wUp = False
                elif carsetup.wUp == False:
                    if carsetup.w >= carsetup.wMin:
                        whiper1.applyRotation([0, 0.05, 0], 1)
                        whiper2.applyRotation([0, 0.05, 0], 1)
                        carsetup.w -= 0.05
def main(controller):
	#get the car object
	car = controller.owner
	
	#check if car was initialized
	if not carsetup.carInitialized(car):
		
		#initialize the car
		_initialize(controller)
		
		#exit
		return
	
	#build the car constraint
	vehicleID = _constraintID(car)
	
	#set tire grip
	carsetup.tireGrip(car, vehicleID)
	
	#set suspension compression
	carsetup.suspensionCompression(car, vehicleID)
	
	#set suspension damping
	carsetup.suspensionDamping(car, vehicleID)
	
	#set suspension stiffness
	carsetup.suspensionStiffness(car, vehicleID)
	
	#set suspension roll influence
	carsetup.suspensionRollInfluence(car, vehicleID)
	
	#run powertrain
	_powertrain(controller, car)
	
	#run powertrain
	_steer(controller, car)
	_whipers(controller, car)
	
	if "Gas" in controller.sensors:
		gas = controller.sensors["Gas"]
	if gas:
		if gas.positive:
			pass
		else:
			if car["CurrentGear"] == -1:
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.01), 2)
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.01), 3)
			elif car["CurrentGear"] == 0:
				vehicleID.applyBraking(0, 2)
				vehicleID.applyBraking(0, 3)
			elif car["CurrentGear"] == 1:
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.01), 2)
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.01), 3)
			elif car["CurrentGear"] == 2:
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.01), 2)
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.01), 3)
			elif car["CurrentGear"] == 3:
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.01), 2)
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.01), 3)
			elif car["CurrentGear"] == 4:
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.01), 2)
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.01), 3)
			elif car["CurrentGear"] == 5:
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.01), 2)
				vehicleID.applyBraking(carsetup.MaxSpeed_5G/(carsetup.Speed + 0.01), 3)