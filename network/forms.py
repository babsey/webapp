from django import forms
import numpy as np

from network.models import Network
from network.helpers import values_extend


class NetworkForm(forms.ModelForm):
    """
    Form for network object, fields are duration and seed
    """
    
    duration = forms.FloatField(help_text="Enter value, which is divisible by 50.")
    seed = forms.IntegerField(help_text="Enter only positive value.")   
    
    class Meta:
        model = Network
        fields = ('duration', 'seed')

    def as_div(self):
        return self._html_output(u'<div class="field-wrapper" title="%(help_text)s">%(label)s %(errors)s %(field)s</div>', u'%s', '</div>', u'%s', False)
        
    def clean_duration(self):
	duration = self.cleaned_data.get('duration')
	
	# duration value should be divisible by 50, it's because of the visualization with protovis.
	if float(duration) % 50 != 0.0:
	    raise forms.ValidationError('This value isn`t divisible by 50.')
	return duration


class DeviceForm(forms.Form):
    """
    Parent form with common fields.
    """    
    
    def __init__(self, network_obj=None, *args, **kwargs):
	self.instance = network_obj
	super(DeviceForm, self).__init__(*args, **kwargs)
    
    model = forms.CharField(max_length=32, widget=forms.HiddenInput())
    targets = forms.CharField(max_length=1000, required=False, help_text="Enter only ID of neurons, e.g. '1,2,4' or '1-3'")
    weight = forms.CharField(max_length=1000, required=False, initial=1.0, help_text="Enter either positive or negative values.")
    delay = forms.CharField(max_length=1000, required=False, initial=1.0, help_text="Enter only positive values is lower than 10 seconds.")
    
    def as_div(self):
        return self._html_output(u'<div class="field-wrapper" title="%(help_text)s">%(label)s %(errors)s %(field)s</div>', u'%s', '</div>', u'%s', False)

    def clean_targets(self):
	targets = self.cleaned_data.get('targets')

	if targets:
	    
	    # Extend targets , e.g. from 1-3 to 1,2,3
	    try:
		extended_list = values_extend(targets, unique=True)
	    except:
		raise forms.ValidationError('enter only number.')
	    
	    # Check if all targets are neurons
    
	    for target in extended_list:
		neuron_ids = self.instance.neuron_ids()
		if not target in neuron_ids:
		    raise forms.ValidationError('targets should be neurons')
	    
	return targets

    def clean_weight(self):
	weight = self.cleaned_data.get('weight')
	if weight:
	    weights = weight.split(',')

	    try:
		weights = np.array([float(val) for val in weights])
	    except:
		raise forms.ValidationError('enter only number')

	    # all weight values of that device are either positive or negative.
	    negative_weights, positive_weights = weights < 0, weights >= 0
	    if not negative_weights.all() and not positive_weights.all():
		raise forms.ValidationError('use either positive or negative values')
	    
	return weight
	
    def clean_delay(self):
	delay = self.cleaned_data.get('delay')
	if delay:
	    delays = delay.split(',')

	    try:
		delays = np.array([float(val) for val in delays])
	    except:
		raise forms.ValidationError('enter only numbers')
	    
	    # delay shouldn't be negative.
	    negative_delays = delays < 0
	    if negative_delays.any():
		raise forms.ValidationError('use only positive values')
	    
	    # delay shouldn't be more than 10s.
	    if max(delays) > 10.0:
		raise forms.ValidationError('delay is too high')
	    
	return delay


""" Neurons as child forms of DeviceForm """
class IafPscAlphaForm(DeviceForm):
    I_e = forms.FloatField(required=False,)
    tau_m = forms.FloatField(required=False,)
    V_th = forms.FloatField(required=False,)
    E_L = forms.FloatField(required=False,)
    t_ref = forms.FloatField(required=False,)
    V_reset = forms.FloatField(required=False,)
    C_m = forms.FloatField(required=False,)
    V_m = forms.FloatField(required=False,)

class ParrotNeuronForm(DeviceForm):
    t_spike = forms.FloatField(required=False,)

""" Inputs as child forms of DeviceForm """
class ACGeneratorForm(DeviceForm):
    amplitude = forms.FloatField(required=False,)
    frequency = forms.FloatField(required=False,)

class DCGeneratorForm(DeviceForm):
    amplitude = forms.FloatField(required=False,)

class NoiseGeneratorForm(DeviceForm):
    start = forms.FloatField(required=False,)
    stop = forms.FloatField(required=False,)
    mean = forms.FloatField(required=False,)
    std = forms.FloatField(required=False,)

class PoissonGeneratorForm(DeviceForm):
    start = forms.FloatField(required=False,)
    stop = forms.FloatField(required=False,)
    rate = forms.FloatField(required=False,)

class SpikeGeneratorForm(DeviceForm):
    start = forms.FloatField(required=False,)
    stop = forms.FloatField(required=False,)
    spike_times = forms.CharField(max_length=1000, required=False,)
    spike_weights = forms.CharField(max_length=1000, required=False,)
    
    def clean_spike_times(self):
	spike_times = self.cleaned_data.get('spike_times')
	if spike_times:
	    spike_times_list = spike_times.split(',')

	    try:
		spike_time_list = np.array([float(val) for val in spike_times_list])
	    except:
		raise forms.ValidationError('enter only numbers')
	    
	return spike_times
	
    def clean_spike_weights(self):
	spike_weights = self.cleaned_data.get('spike_weights')
	if spike_weights:
	    spike_weights_list = spike_weights.split(',')

	    try:
		spike_weights_list = np.array([float(val) for val in spike_weights_list])
	    except:
		raise forms.ValidationError('enter only numbers')
	    
	return spike_weights    

""" Outputs as entire forms """

class SpikeDetectorForm(forms.Form):
    def __init__(self, network_obj=None, *args, **kwargs):
	self.instance = network_obj
	super(SpikeDetectorForm, self).__init__(*args, **kwargs)
	
    model = forms.CharField(max_length=32, widget=forms.HiddenInput())
    sources = forms.CharField(max_length=1000, help_text="Enter only ID of neurons, e.g. '1,2,4' or '1-3'")
    
    def as_div(self):
        return self._html_output(u'<div class="field-wrapper" title="%(help_text)s">%(label)s %(errors)s %(field)s</div>', u'%s', '</div>', u'%s', False)
        
    def clean_sources(self):
	sources = self.cleaned_data.get('sources').replace(' ','')
	try:
	    extended_list = values_extend(sources, unique=True)
	except:
	    raise forms.ValidationError('enter only number.')
	
	# check if all sources are neurons
	for source in extended_list:
	    neuron_ids = self.instance.neuron_ids()
	    if not source in neuron_ids:
		raise forms.ValidationError('sources should be neurons')
	    
	return sources
	
class VoltmeterForm(forms.Form):
    def __init__(self, network_obj=None, *args, **kwargs):
	self.instance = network_obj
	super(VoltmeterForm, self).__init__(*args, **kwargs)
	
    model = forms.CharField(max_length=32, widget=forms.HiddenInput())
    targets = forms.CharField(max_length=1000, help_text="Enter only ID of neurons, e.g. '1,2,4' or '1-3'")
    
    def as_div(self):
        return self._html_output(u'<div class="field-wrapper" title="%(help_text)s">%(label)s %(errors)s %(field)s</div>', u'%s', '</div>', u'%s', False)
	    
    def clean_targets(self):
	targets = self.cleaned_data.get('targets').replace(' ','')
	try:
	    extended_list = values_extend(targets, unique=True)
	except:
	    raise forms.ValidationError('enter only number.')
	
	# check if all targets are neurons
	for target in extended_list:
	    neuron_ids = self.instance.neuron_ids()
	    if not target in neuron_ids:
		raise forms.ValidationError('targets should be neurons')
	    
	return targets
