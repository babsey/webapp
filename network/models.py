from django.contrib.auth.models import User
from django.db import models

import cjson


SPIC_CHOICES = (
	('1','SPIC1'),
	('2','SPIC2'),
	('3','SPIC3'),
	('4','SPIC4')
)

class Network(models.Model):
    user_id = models.IntegerField()
    SPIC_id = models.CharField(max_length=6, choices=SPIC_CHOICES)
    local_id = models.IntegerField()
    
    title = models.CharField(null=True, blank=True, max_length=32)
    description = models.TextField(blank=True)    
    
    duration = models.FloatField(null=True, default=500.0)
    seed = models.IntegerField(null=True, default=1)
    status_json = models.TextField(blank=True, verbose_name='Root status')
    devices_json = models.TextField(blank=True, verbose_name='Devices')
    
    def user(self):
	"""
	Gets user object from the django model 'auth' by user_id.
	CAUTION: the model 'auth' might be stored in other database.
	"""
	
	if self.user_id == 0:
	    return 'architect'
	else:
	    return User.objects.get(pk=self.user_id)

    def __unicode__(self):
        return '%s_%s_%s' %(self.user(), self.get_SPIC_id_display(), self.local_id)

    def root_status(self):
	"""
	Returns status data from the field status_json.
	"""
	if self.status_json:
	    return cjson.decode(self.status_json)
	return []

    def device_list(self, modeltype=None):
	"""
	Returns a list of devices by loading JSON from the field devices_json.
	Argument modeltype is for filtering devices by its type,
	its default is None, choices are 'neuron', 'input' or 'output'.
	"""
	if self.devices_json:
	    devices = cjson.decode(self.devices_json)
	    
	    if modeltype:
		return [dev for dev in devices if dev[1]['type']==modeltype]
	    return devices
	return []
    
    def last_device_id(self):
	"""
	Returns in case of existing devices the last ID of device 
	as a marker for adding new device. Otherwise it returns None.
	"""
	
	device_list = self.device_list()
	if device_list:
	    return device_list[-1][0]
	return 0
	
    
    def get_devices(self, label, modeltype=None):
	""" 
	Returns a list of devices from the field device_json by label.
	Optional: filter is enter a modeltype of device before.	
	"""
	
	device_list = self.device_list(modeltype)
	if device_list:
	    return [dev for dev in device_list if dev[1]['label'] == label]
	return device_list
	
    def has_device(self, label, modeltype=None):
	""" Returns existence of device in the field device_json by label."""
	
	device_list = self.device_list(modeltype)
	if device_list:
	    return [dev for dev in device_list if dev[1]['label'] == label] > 0
	return False

    def neuron_ids(self):
	"""
	Gets a list of neuron ID for connectivity matrix and
	validation check of targets/sources.
	"""
	
	neuron_list = self.device_list('neuron')
	if neuron_list:
	    return [int(dev[0]) for dev in neuron_list]
	return neuron_list
	
    def weight_list(self):
	"""
	Gets a listed tuple of device ID and list of weights for connectivity matrix.
	"""
	
	device_list = self.device_list()
	w_list = []
	if device_list:
	    for gid, model, status, params in device_list:
		if 'weight' in params:
		    weights = []
		    try:
			targets = params['targets'].split(',')
			targets = [int(tgt) for tgt in targets]
			weight = params['weight'].split(',')
		    except:
			targets = []
			
		    for neuron_id, neuron_model, neuron_status, neuron_params in self.device_list('neuron'):
			if neuron_id in targets:
			    try:
				weights.append(u'%s' %weight[targets.index(neuron_id)%len(weight)])
			    except:
				weights.append(u'%s' %weight[0])
			else:
			    weights.append(u' ')
		    w_list.append((gid, weights))
	return w_list
	
    def delay_list(self):
	"""
	Gets a listed tuple of device ID and list of delays for connectivity matrix.
	"""
	
	device_list = self.device_list()
	d_list = []
	if device_list:
	    for gid, model, status, params in device_list:
		if 'delay' in params:
		    delays = []
		    try:
			targets = params['targets'].split(',')
			targets = [int(tgt) for tgt in targets]
			delay = params['delay'].split(',')
		    except:
			targets = []
			
		    for neuron_id, neuron_model, neuron_status, neuron_params in self.device_list('neuron'):
			if neuron_id in targets:
			    try:
				delays.append(u'%s' %delay[targets.index(neuron_id)%len(delay)])
			    except:
				delays.append(u'%s' %delay[0])
			else:
			    delays.append(u' ')
		    d_list.append((gid, delays))
	return d_list

    def connections(self, data=False, modeltype=None):
	"""
	Gets a listed tuple of source and target in each connection.
	If data is True, it also returns dictionary of weight and delay.
	modeltype default is None, choices are 'neuron', 'input' or 'output'.
	-> see the method device_list.
	"""	
	device_list = self.device_list(modeltype)
	connections = []
	if device_list:
	    if modeltype == 'IO_device':
		connections.extend(self.connections(data=data, modeltype='input'))
		connections.extend(self.connections(data=data, modeltype='output'))
	    else:
		for gid, model, status, params in device_list:
		    if params:
			if model['label'] == u'spike_detector':
			    if len(params['sources']) > 0:
				sources = params['sources'].split(',')
				for index, source in enumerate(sources):
				    if data:
					connections.append([int(source), gid,  None])
				    else:
					connections.append([int(source), gid])
			    
			else:
			    if len(params['targets']) > 0:
				targets = params['targets'].split(',')
				for index, target in enumerate(targets):
				    if data:
					connection_params = {}
					if 'weight' in params:
					    weights = params['weight'].split(',')
					    connection_params['weight'] = float(weights[index%len(weights)])
					if 'delay' in params:
					    delays = params['delay'].split(',')
					    connection_params['delay'] = float(delays[index%len(delays)])
					    
					if connection_params: 
					    connections.append([gid, int(target), connection_params])
					else:
					    connections.append([gid, int(target), {}])
				    else:
					connections.append([gid, int(target)])
	return connections

    def connect_to(self, modeltype):
	device_list = self.device_list(modeltype)
	neurons = []
	for dev in device_list:
	    if 'targets' in dev[3]:
		neurons.extend(dev[3]['targets'].split(','))
	    else:
		neurons.extend(dev[3]['sources'].split(','))
	if neurons:
	    
	    neurons = [int(ii) for ii in neurons if ii != '']
	return list(set(neurons))
	
    def connect_to_input(self):
	return self.connect_to('input')
	
    def connect_to_output(self):
	return self.connect_to('output')	
	
    def neurons(self):
	""" Returns a readable string of all neurons."""
	
	neuron_list = self.device_list('neuron')
	if neuron_list:
	    neuron_list = [(dev[1]['label'], int(dev[0])) for dev in neuron_list]
	    if len(neuron_list) < 20:
		return ", ".join(["%s [%s]"%neuron for neuron in neuron_list])
	    else:
		return '%s neurons' %len(neuron_list)
	return ""

    def	inputs(self):
	""" Returns a readable string of all inputs."""
	
	input_list = self.device_list('input')
	if input_list:
	    return ", ".join(["%s [%s]"%(ii[1]['label'],ii[0]) for ii in input_list])
	return ""
	
    def	outputs(self):
	""" Returns a readable string of all outputs."""
	
	output_list = self.device_list('output')
	if output_list:
	    return ", ".join(["%s [%s]"%(oo[1]['label'],oo[0]) for oo in output_list])
	return ""