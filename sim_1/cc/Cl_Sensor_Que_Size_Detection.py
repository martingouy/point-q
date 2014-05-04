import Cl_Sensor
import List_Explicit_Values

class Sensor_Que_Size_Detection(Cl_Sensor.Sensor):

	def __init__(self,val_id_sens=-1,val_id_link_sens_location=-1,\
	val_id_que_destination_link_sens_location=-1, val_init_que_position_measured_by_sens=-1):
	#,\
	#val_que_size_reached=None):
	
		Cl_Sensor.Sensor.__init__(self,val_id_sensor=val_id_sens,\
		val_type_sensor=Cl_Sensor.TYPE_SENSOR["sensor_que_size_detect"],\
		val_id_link_sensor_location=val_id_link_sens_location,\
		val_id_que_destination_link_sensor_location=val_id_que_destination_link_sens_location,\
		val_init_que_position_measured_by_sensor=val_init_que_position_measured_by_sens)
		
		
#*****************************************************************************************************************************************************************************************
	
	#method requiesting the sensor about its current state (detect whether the que size has reached a given value)
	def fct_request_state_sensor_que_size_detection(self,val_network):
	
		#if the que length is at least the val that the detector captures 
		if len(val_network.get_di_entry_internal_links()[self._id_link_sensor_location].get_set_veh_queue().get_di_obj_veh_queue_at_link()\
		[self._id_link_sensor_location,self._id_que_destination_link_sensor_location].get_queue_veh())>=self._init_que_position_measured_by_sensor:
		#-1:
		
			return List_Explicit_Values.initialisation_value_to_one
		
		#if the que length is at less the val that the detector captures 
		else:
			return List_Explicit_Values.initialisation_value_to_zero
		
#*****************************************************************************************************************************************************************************************
		
		
	