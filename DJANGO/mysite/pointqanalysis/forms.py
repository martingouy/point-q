from django import forms
import tools_data

def validate_file_extension(value):
	if not value.name.endswith('.txt'):
		raise forms.ValidationError(u'Error: Wrong file extension')

def get_my_choices():

	# we create the table index_network if it's not created
    #	query_1 = 'CREATE TABLE index_network (name text, geojson text)'
	query_1 = 'CREATE TABLE index_network (name text, geojson text, topjson text)'
	tools_data.query_sql([query_1], False, 'network_db')

	query_2 = 'SELECT name FROM index_network'
	output = tools_data.query_sql([query_2], True, 'network_db')
	liste_name = []
	for line in output:
		liste_name.append((line['name'], line['name']))
	
	return liste_name
        
class Form_upload_fil (forms.Form):

	def __init__(self, *args, **kwargs):
		super(Form_upload_fil, self).__init__(*args, **kwargs)

		# creates a tuple of the available networks
		self.fields['name_network'] = forms.ChoiceField(choices=get_my_choices())

	name_simul = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name Simulation', 'class': 'form-control'}))
	simul_txt_db = forms.FileField(validators=[validate_file_extension])
    
class Form_upload_xml (forms.Form):
	name_network = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name Network', 'class': 'form-control'}))
	network_xml = forms.FileField()

class Form_delete_xml (forms.Form):

	def __init__(self, *args, **kwargs):
		super(Form_delete_xml, self).__init__(*args, **kwargs)

		# creates a tuple of the available networks
		choices=get_my_choices()
		choices.append(('',''))
		self.fields['name_network_delete'] = forms.ChoiceField(choices)
