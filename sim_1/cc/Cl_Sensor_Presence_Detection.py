import Cl_Sensor
import  List_Explicit_Values

class Sensor_Presence_Detection(Cl_Sensor.Sensor):

	def __init__(self,val_id_sens=-1,val_id_link_sens_location=-1,\
	val_id_que_destination_link_sens_location=-1, val_init_que_position_measured_by_sens=-1,\
	val_final_que_position_measured_by_sensor=-1,val_answer_sens_last_require=None):
	
		Cl_Sensor.Sensor.__init__(self,val_id_sensor=val_id_sens,\
		val_type_sensor=Cl_Sensor.TYPE_SENSOR["sensor_presence_detect"],\
		val_id_link_sensor_location=val_id_link_sens_location,\
		val_id_que_destination_link_sensor_location=val_id_que_destination_link_sens_location,\
		val_init_que_position_measured_by_sensor=val_init_que_position_measured_by_sens)
		
		#the final que location measured (captured) by the sensor, the 1st position is indicated by number one
		self._final_que_position_measured_by_sensor=val_final_que_position_measured_by_sensor


		#the sensor answer at last demand 
		self._answer_sens_last_require=val_answer_sens_last_require
		
#*****************************************************************************************************************************************************************************************
	#method returning the final position of the que captured by the detector
	def get_final_que_position_measured_by_sensor(self):
		return self._final_que_position_measured_by_sensor
	
#*****************************************************************************************************************************************************************************************
	#method returning the sensor answer when last required
	def get_answer_sens_last_require(self):
		return self._answer_sens_last_require
#*****************************************************************************************************************************************************************************************
	#method modifying the sensor answer when last required
	def set_answer_sens_last_require(self,n_v):
		self._answer_sens_last_require=n_v
#*****************************************************************************************************************************************************************************************
	#method modifying the final position of the  que region recorded by the detector
	def set_final_que_position_measured_by_sensor(self,n_v):
		self._final_que_position_measured_by_sensor=n_v
	
#*****************************************************************************************************************************************************************************************
	#method requiesting the sensor about its current state (detect whether the que size has reached a given value)
	def fct_request_state_sensor_presence_detection(self,val_network):
	
		#if there are vehicles within the detector's area (the que size has the desired width of elements)
		if len(val_network.get_di_entry_internal_links()[self._id_link_sensor_location].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_link_sensor_location,self._id_que_destination_link_sensor_location].get_queue_veh()\
		[self._init_que_position_measured_by_sensor-1:self._final_que_position_measured_by_sensor+1])>0:
		
			return List_Explicit_Values.initialisation_value_to_one
		#if there are no vehicles within the detector's area 
		else:
			return List_Explicit_Values.initialisation_value_to_zero
		

#*****************************************************************************************************************************************************************************************