import List_Explicit_Values

TYPE_SENSOR={"sensor_presence_detect":1,"sensor_que_size_detect":2}

class Sensor:

	def __init__(self,val_id_sensor=-1,val_type_sensor=None,val_id_link_sensor_location=-1,\
	val_id_que_destination_link_sensor_location=-1,val_init_que_position_measured_by_sensor=-1):


		#the id if the sensor
		self._id_sensor=val_id_sensor
	
		#the type of the sensor
		self._type_sensor=val_type_sensor
	
		#the id of the id where the sensor was located
		self._id_link_sensor_location=val_id_link_sensor_location
	
		#the id of the destination link case when the sensor is located in a que
		self._id_que_destination_link_sensor_location=val_id_que_destination_link_sensor_location
		
		
		#the initial que region measured (captured) by the sensor, the 1st position is indicated by number one
		self._init_que_position_measured_by_sensor=val_init_que_position_measured_by_sensor
		
		
		#the answered returned by the sensor
		#self._answer_sensor=val_answer_sensor
	
#*****************************************************************************************************************************************************************************************
	#method returning the sensor id
	def get_id_sensor(self):
		return self._id_sensor
#*****************************************************************************************************************************************************************************************
	#method returning the type of the sensor
	def get_type_sensor(self):
		return self._type_sensor

#*****************************************************************************************************************************************************************************************
	#method returning the id of link where the sensor is placed
	def get_id_link_sensor_location(self):
		return self._id_link_sensor_location
	
#*****************************************************************************************************************************************************************************************
	#method returning the id of destination link of the que when the sensor is located in a queue
	def get_id_que_destination_link_sensor_location(self):
		return self._id_que_destination_link_sensor_location
	
#*****************************************************************************************************************************************************************************************
	#method returning the  initial position of the que region captured by the detector
	def get_init_que_position_measured_by_sensor(self):
		return self._init_que_position_measured_by_sensor
	
#*****************************************************************************************************************************************************************************************
	
	#method returning the answer returned by the sensor
	#def get_answer_sensor(self):
		#return self._answer_sensor

#*****************************************************************************************************************************************************************************************
	#method modifying the sensor id
	def set_id_sensor(self,n_v):
		self._id_sensor=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the type of the sensor
	def set_type_sensor(self,n_v):
		self._type_sensor=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying  the id of link where the sensor is placed
	def set_id_link_sensor_location(self,n_v):
		self._id_link_sensor_location=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the id of destination link of the que when the sensor is located in a queue
	def set_id_que_destination_link_sensor_location(self,n_v):
		self._id_que_destination_link_sensor_location=n_v
	
#*****************************************************************************************************************************************************************************************
	#method modifying the initial position of the  que region recorded by the detector
	def set_init_que_position_measured_by_sensor(self,n_v):
		self._init_que_position_measured_by_sensor=n_v
	
#*****************************************************************************************************************************************************************************************

	#method modifying the answer returned by the sensor
	#def set_answer_sensor(self,n_v):
		#self._answer_sensor=n_v

#*****************************************************************************************************************************************************************************************

	#method requiesting the sensor about its current state (detect whether the que size has reached a given value)
	def fct_request_state_sensor_1(self,val_network):
	
		#if the que length is at least the val that the detector captures 
		if len(val_network.get_di_entry_internal_links()[self._id_link_sensor_location].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_link_sensor_location,self._id_que_destination_link_sensor_location].get_queue_veh())>=self._que_position_measured_by_sensor-1:
		
			return List_Explicit_Values.initialisation_value_to_one
		
		#if the que length is at less the val that the detector captures 
		else:
			return List_Explicit_Values.initialisation_value_to_zero
		
#*****************************************************************************************************************************************************************************************









































	