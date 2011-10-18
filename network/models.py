# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
import numpy as np

import lib.json as json
from network.helpers import id_escape

__all__ = ["Network"]

SPIC_CHOICES = (('0','Sandbox'),
                ('1','SPIC1'),
                ('2','SPIC2'),
                ('3','SPIC3'),
                ('4','SPIC4'))

class Network(models.Model):
    user_id = models.IntegerField()
    SPIC_id = models.CharField(max_length=6, choices=SPIC_CHOICES)
    local_id = models.IntegerField()
    
    title = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    
    duration = models.FloatField(null=True, default=1000.0)
    status_json = models.TextField(blank=True, verbose_name='Root status')
    devices_json = models.TextField(blank=True, verbose_name='Devices')

    def __unicode__(self):
        return '%s_%s_%s' %(self.user(), self.get_SPIC_id_display(), self.local_id)

    def user(self):
        """
        Get user object from the django model 'auth' by user_id.
        CAUTION: the model 'auth' might be stored in other database.
        """
        if self.user_id == 0:
            return 'architect'
        else:
            return User.objects.get(pk=self.user_id)

    def root_status(self):
        """ Returns status data from the field status_json."""
        if self.status_json:
            return json.decode(str(self.status_json))
        return {}

    def layout_size(self):
        x, y = 260, 12
        for dev in self.device_list(modeltype='neuron'):
            if 'position' in dev[0]:
                pos = dev[0]['position']
                if pos[0] > x:
                    x = pos[0]
                if pos[1] > y:
                    y = pos[1]
        return {'x':x, 'y':y}

    def id_filterbank(self):
        device_dict = self.device_dict()
        device_items = device_dict.items()
        device_items.sort()

        ids = []
        for tid, device in device_items:
            if 'id' in device[0]:
                ids.append((tid, int(device[0]['id'])))
            else:
                ids.append((tid, -1))
                
        return np.array(ids, dtype=int)

    def device_dict(self):
        """
        Return a dict of devices by loading JSON from the field devices_json.
        """
        if self.devices_json:
            return json.decode(str(self.devices_json))
        return []

    def device_list(self, term='visible', modeltype=None, label=None, key=None):
        """
        Return a list of devices.
        Argument modeltype is for filtering devices by its type,
        its default is None, choices are 'neuron', 'input' or 'output'.
        """
        device_dict = self.device_dict()
        if device_dict:
            device_items = device_dict.items()
            device_items.sort()
                                    
            if term == 'all':
                device_list = [dev[1] for dev in device_items]
                
            elif term == 'visible':
                id_filterbank = self.id_filterbank()
                device_list = [dev[1] for dev in device_items if 'id' in dev[1][0]]
                
                for idx, dev in enumerate(device_list):
                    if 'targets' in dev[2]:
                        targets = dev[2]['targets'].split(',')
                        if not 'voltmeter' in dev[0]['label']:
                            delays = dev[2]['delay'].split(',')
                            weights = dev[2]['weight'].split(',')
                        else:
                            delays, weights = [], []

                        new_targets = []
                        new_weights, new_delays = [], []
                        for idx_tgt, tgt in enumerate(targets):
                            if tgt:
                                tid = ('%4d' %int(tgt)).replace(' ', '0')
                                new_tgt = id_escape(id_filterbank, tid)
                            
                                if new_tgt > 0:
                                    new_targets.append(str(new_tgt))
                                    if len(weights) > 1:
                                        new_weights.append(weights[idx_tgt])
                                    elif weights:
                                        new_weights = weights
                                
                                    if len(delays) > 1:
                                        new_delays.append(delays[idx_tgt])
                                    elif delays:
                                        new_delays = delays
                                
                        device_list[idx][2]['targets'] = ','.join(new_targets)
                        if not 'voltmeter' in dev[0]['label']:
                            device_list[idx][2]['weight'] = ','.join(new_weights)
                            device_list[idx][2]['delay'] = ','.join(new_delays)

                    if 'sources' in dev[2]:
                        sources = dev[2]['sources'].split(',')

                        new_sources = []
                        for idx_src, src in enumerate(sources):
                            if src:
                                tid = ('%4d' %int(src)).replace(' ', '0')
                                new_src = id_escape(id_filterbank, tid)

                                if new_src > 0:
                                    new_sources.append(str(new_src))
                                
                        device_list[idx][2]['sources'] = ','.join(new_sources)

            elif term == 'hidden':
                device_list = [dev[1] for dev in device_items if not 'id' in dev[1][0]]
                
            if modeltype:
                device_list = [dev for dev in device_list if dev[0]['type'] == modeltype]
            if label:
                device_list = [dev for dev in device_list if dev[0]['label'] == label]
            if key:
                if key in ['id','label','type','position']:
                    device_list = [dev[0][key] for dev in device_list if key in dev[0]]
                elif key in ['targets','sources','weight','delay']:
                    device_list = [dev[2][key] for dev in device_list if key in dev[2]]
                else:
                    device_list = [dev[1][key] for dev in device_list if key in dev[1]]
                
            return device_list
        return device_dict

    def last_device_id(self):
        """
        Return in case of existing devices the last ID of device 
        as a marker for adding new device. Otherwise it returns None.
        """
        device_list = self.device_list()
        if device_list:
            return device_list[-1][0]['id']
        return 0
    
    def has_device(self, label, modeltype=None, term='visible'):
        """ Returns existence of device in the field device_json by label."""
        device_list = self.device_list(term, modeltype=modeltype, label=label)
        if device_list:
            return True
        return False

    def neuron_ids(self):
        """
        Get a list of neuron ID for connectivity matrix and
        validation check of targets/sources.
        """
        neuron_list = self.device_list(modeltype='neuron')
        if neuron_list:
            return [int(dev[0]['id']) for dev in neuron_list]
        return neuron_list
        
    def neuron_ids_to_spike_detector(self):
        return self.neuron_ids(connect_to='spike_detector')

    def neuron_id_filterbank(self, modeltype=None, label=None):
        neuron_list = self.device_list(modeltype='neuron')
        
        if modeltype or label:
             neuron_ids = self._connect_to(modeltype=modeltype, label=label)
             neuron_list = [neuron for neuron in neuron_list if neuron[0]['id'] in neuron_ids]
        return np.array([[neuron[0]['id'], gid+1] for gid, neuron in enumerate(neuron_list)])
            
    def _get_param_list(self, term):
        """
        Get a listed tuple of device ID and list of values 
        for connectivity matrix for weight or delay.
        """
        device_list = self.device_list()
        value_list = []
        if device_list:
            for model, status, conns in device_list:
                if term in conns:
                    values = []
                    try:
                        targets = conns['targets'].split(',')
                        targets = [int(tgt) for tgt in targets]
                        value = conns[term].split(',')
                    except:
                        targets = []
                        
                    for neuron_model, neuron_status, neuron_conns in self.device_list(modeltype='neuron'):
                        if int(neuron_model['id']) in targets:
                            try:
                                values.append(u'%s' %value[targets.index(int(neuron_model['id']))%len(value)])
                            except:
                                values.append(u'%s' %value[0])
                        else:
                            values.append(u' ')
                    value_list.append((model['id'], values))
        return value_list
        
    def weight_list(self):
        """ Get a listed tuple for weight. """
        return self._get_param_list('weight')
        
    def delay_list(self):
        """ Get a listed tuple of delay. """
        return self._get_param_list('delay')

    def connections(self, term='visible', data=False, modeltype=None):
        """
        Get a listed tuple of source and target in each connection.
        If data is True, it also returns dictionary of weight and delay.
        modeltype default is None, choices are 'neuron', 'input' or 'output'.
        -> see the method device_list.
        """        
        device_list = self.device_list(term, modeltype=modeltype)
        neuron_id_filterbank = self.neuron_id_filterbank()

        connections = []
        if device_list:
            if modeltype == 'IO_device':
                connections.extend(self.connections(term=term, data=data, modeltype='input'))
                connections.extend(self.connections(term=term, data=data, modeltype='output'))
            else:
                for gid, device in enumerate(device_list):
                    model, status, conns = device
                    gid += 1
                    #if 'id' in model:
                        #assert gid == int(model['id'])
                        
                    if conns:
                        if 'sources' in conns:
                            if len(conns['sources']) > 0:
                                sources = conns['sources'].split(',')
                                for index, source in enumerate(sources):
                                  
                                    if data:
                                        connections.append([int(source), gid,  {}, ''])
                                    else:
                                        connections.append([int(source), gid])
                            
                        elif 'targets' in conns:
                            if len(conns['targets']) > 0:
                                targets = conns['targets'].split(',')
                                for index, target in enumerate(targets):
                                        
                                    if target:
                                        if modeltype == 'neuron':
                                            target = id_escape(neuron_id_filterbank, target)
                                            
                                        if data:
                                            connection_params, connection_model = {}, ''
                                            if 'weight' in conns:
                                                weights = conns['weight'].split(',')
                                                connection_params['weight'] = float(weights[index%len(weights)])
                                            if 'delay' in conns:
                                                delays = conns['delay'].split(',')
                                                connection_params['delay'] = float(delays[index%len(delays)])
                                            if 'synapse_type' in conns:
                                                connection_models = conns['synapse_type']
                                                connection_model = connection_models[index%len(connection_models)]
                                            
                                            if connection_model:
                                                connections.append([gid, int(target), connection_params, connection_model])
                                            elif connection_params: 
                                                connections.append([gid, int(target), connection_params, ''])
                                            else:
                                                connections.append([gid, int(target), {}, ''])
                                        else:
                                            connections.append([gid, int(target)])
        return connections
        
    def edgelist(self):
        """ Get a list of neoron edges for graph. """
        return self.connections(data=True, modeltype='neuron')

    def _connect_to(self, modeltype=None, label=None):
        """ Get a list of devices of one type, which the neurons are connected to. """
        device_list = self.device_list(modeltype=modeltype, label=label)
        neurons = []
        for model, status, conns in device_list:
            if 'targets' in conns:
                neurons.extend(conns['targets'].split(','))
            else:
                neurons.extend(conns['sources'].split(','))
        if neurons:
            neurons = [int(nn) for nn in neurons if nn != '']
        return list(set(neurons))
        
    def connect_to_input(self):
        """ List of connections of neurons are connected to input. """
        return self._connect_to(modeltype='input')
        
    def connect_to_output(self):
        """ List of connections of neurons are connected to output. """
        return self._connect_to(modeltype='output')    
        
    def connect_to_spike_detector(self):
        """ List of connections of neurons are connected to output. """
        return self._connect_to(label='spike_detector')            
        
    def neurons(self):
        """ Return a readable string of all meurons. """        
        neuron_list = self.device_list(modeltype='neuron')
        if neuron_list:
            neuron_list = [(nn[0]['label'], nn[0]['id']) for nn in neuron_list]
            if len(neuron_list) < 20:
                return ", ".join(["%s [%s]"% neuron for neuron in neuron_list])
            else:
                return "%s neurons" % len(neuron_list)
        return ""

    def inputs(self):
        """ Return a readable string of all inputs. """        
        input_list = self.device_list(modeltype='input')
        if input_list:
            return ", ".join(["%s [%s]"%(ii[0]['label'],ii[0]['id']) for ii in input_list])
        return ""
        
    def outputs(self):
        """ Return a readable string of all outputs. """        
        output_list = self.device_list(modeltype='output')
        if output_list:
            return ", ".join(["%s [%s]"%(oo[0]['label'],oo[0]['id']) for oo in output_list])
        return ""