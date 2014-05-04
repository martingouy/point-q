import List_Explicit_Values
import heapq
from heapq import *



#TYPE_EV={"type_ev_end_decision_next_intersection_control":2}
TYPE_EV={"type_ev_veh_appearance":1,"type_ev_end_decision_next_intersection_control":2,"type_ev_new_intersection_control":3,\
"type_ev_end_veh_departure_from_que":4,"type_ev_veh_arrived_at_que":5,"ty_ev_end_veh_hold_at_que":6,\
"ty_ev_veh_flow_changes":7,"type_ev_veh_appearance_nsi":8,"ty_ev_end_veh_hold_at_que_nsi":9,\
"type_ev_end_veh_departure_from_que_nsi":10,"type_ev_veh_arrived_at_que_nsi":11}


class Event:

	"Class base defining an event object"
	
	def __init__(self,val_event_time=-1,val_event_type=-1,val_global_fct_obj=None,val_global_fct_nsi_obj=None):
	
		#the event time
		self._event_time=val_event_time
		
		#the event type
		self._event_type=val_event_type
		
		#the global functions object
		self._global_fct_obj=val_global_fct_obj
		
		#the global functions object nsi
		self._global_fct_nsi_obj=val_global_fct_nsi_obj
		
		
		
#*****************************************************************************************************************************************************************************************
	#method returning the event time
	def get_event_time(self):
		return self._event_time

#*****************************************************************************************************************************************************************************************
	#method returning the event type
	def get_event_type(self):
		return self._event_type
		
#*****************************************************************************************************************************************************************************************
	#method returning the global function object
	def get_global_fct_obj(self):
		return self._global_fct_obj

#*****************************************************************************************************************************************************************************************
	#method returning the global function nsi object
	def get_global_fct_nsi_obj(self):
		return self._global_fct_nsi_obj

#*****************************************************************************************************************************************************************************************	
	#method modifying the event time
	def set_event_time(self,n_v):
		self._event_time=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the event type
	def set_event_type(self,n_v):
		self._event_type=n_v
		
#*****************************************************************************************************************************************************************************************
	#method modifying the global function object
	def set_global_fct_obj(self,n_v):
		self._global_fct_obj=n_v

#*****************************************************************************************************************************************************************************************
	#method modifying the global function nsi object
	def set_global_fct_nsi_obj(self,n_v):
		self._global_fct_nsi_obj=n_v

#*****************************************************************************************************************************************************************************************
	#method printing an event 
	def print_even_base(self):
	
		""" method printing a basic event """
		print ("----------------------------------------------------------------------------")
		print ("Characteristics  base event: ")
		print("EVENT TYPE",self._event_type)
		print("EVENT TIME",self._event_time)
		print( "----------------------------------------------------------------------------")
		
#*****************************************************************************************************************************************************************************************	
	def __le__(self,other_even):
		return self._event_time<=other_even.get_event_time()
		
#*****************************************************************************************************************************************************************************************
	def __lt__(self,other_even):
		return self._event_time<other_even.get_event_time()

#*****************************************************************************************************************************************************************************************
	#method inserting an event in the event list.
	#if the new inserting event has an event time < of the first event of the heap
	#we print a message and the simulation is interrupted
	def fct_insertion_even_in_event_list(self,event_list,message):
	
		"""method inserting an event in the event list """
		
		#if the event list is not empty
		#if len(event_list) > List_Explicit_Values.initialisation_value_to_zero:
		if event_list!=[]:
		
			#if the event time is < to the time of the first event
			if self._event_time< event_list[List_Explicit_Values.val_first_element_of_list].get_event_time():
			
				print("CURRENT EVENT TIME",self._event_time,"EVENT TYPE",self._event_type)
				print("1ST EVENT LIST",event_list[List_Explicit_Values.val_first_element_of_list].get_event_time(),\
				"EVENT TYPE",self._event_type)
				
				#print("IN FUNCTION INSERTION EVENT, TIME NEW EVENT",self._event_time(),"TIME FIRST EVENT IN THE LIST: ",\
				#event_list[List_Explicit_Values.val_first_element_of_list].get_event_time())
				print (message)
				import sys
				sys.exit()
			
			#if the event time is >= to the time of the first event
			#we insert the event in the list
			else:
				heappush(event_list,self)
				
		#if the event list is empty
		else:
			#on insere l'evenement dans la pile
			heappush(event_list,self)


#*****************************************************************************************************************************************************************************************
#ev=Event(1)
#ev_list=[]
#print(len(ev_list))
#ev.fct_insertion_even_in_event_list(ev_list,"hi")
#print(len(ev_list))
