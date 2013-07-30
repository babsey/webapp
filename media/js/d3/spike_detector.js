function binwidth_changed() {

    options.histogram.binwidth = parseInt($( this ).attr('value'));
    $.cookie('options', options, { expires: 7});

    var hist = d3.layout.histogram()
        .bins(data.spike_detector.time_scale.ticks(parseInt(data.spike_detector.meta.simTime / options.histogram.binwidth)));

    if (!(options.histogram.binwidth in data.spike_detector.hist)) {
        data.spike_detector.hist[options.histogram.binwidth] = {}
        for (var i in data.spike_detector.spikes) {
            data.spike_detector.hist[options.histogram.binwidth][i] = hist(data.spike_detector.spikes[i]);
        }
    }

    draw_histogram("#spike_detector #histogram");
    draw_correlation_plot("#spike_detector #correlation_plot", calc_correlation(data.spike_detector.hist[options.histogram.binwidth][options.correlation.neuronA], data.spike_detector.hist[options.histogram.binwidth][options.correlation.neuronB], 'valid'));
}

function neuronA_changed(e) {
    e.preventDefault();
    options.correlation.neuronA = $(this).attr('value');
    $.cookie('options', options, { expires: 7});

    draw_correlation_plot("#spike_detector #correlation_plot", calc_correlation(data.spike_detector.hist[options.histogram.binwidth][options.correlation.neuronA], data.spike_detector.hist[options.histogram.binwidth][options.correlation.neuronB], 'valid'));
    $(this).parents(".btn-group").find(".title").html("Neuron " + data.spike_detector.meta.neurons[options.correlation.neuronA].id);
}

function neuronB_changed(e) {
    e.preventDefault();
    options.correlation.neuronB = $(this).attr('value');
    $.cookie('options', options, { expires: 7});

    draw_correlation_plot("#spike_detector #correlation_plot", calc_correlation(data.spike_detector.hist[options.histogram.binwidth][options.correlation.neuronA], data.spike_detector.hist[options.histogram.binwidth][options.correlation.neuronB], 'valid'));
    $(this).parents(".btn-group").find(".title").html("Neuron " + data.spike_detector.meta.neurons[options.correlation.neuronB].id);
}

function draw_spike_detector(reference) {

    data.spike_detector.time_scale = d3.scale.linear()
        .domain([0, 1000.])
        .range([0, 1.]);

    var hist = d3.layout.histogram()
        .bins(data.spike_detector.time_scale.ticks(parseInt(data.spike_detector.meta.simTime / options.histogram.binwidth)));

    data.spike_detector.spikes = {};
    for (var i=0; i<data.spike_detector.senders.length; i++) {
        if ( data.spike_detector.senders[i] in data.spike_detector.spikes ) {
            data.spike_detector.spikes[data.spike_detector.senders[i]].push(data.spike_detector.times[i])
        } else {
            data.spike_detector.spikes[data.spike_detector.senders[i]] = [data.spike_detector.times[i]]
        }
    }

    data.spike_detector.hist = {};
    data.spike_detector.hist[options.histogram.binwidth] = {};
    for (var i in data.spike_detector.spikes) {
        data.spike_detector.hist[options.histogram.binwidth][i] = hist(data.spike_detector.spikes[i]);
    }

    $(".binwidth").on('click', binwidth_changed)
    $( "#neuronA li a" ).on('click', neuronA_changed)
    $( "#neuronB li a" ).on('click', neuronB_changed)

    draw_raster_plot(reference +" #raster_plot");
    draw_histogram(reference +" #histogram");
    draw_correlation_plot(reference +" #correlation_plot", calc_correlation(data.spike_detector.hist[options.histogram.binwidth][options.correlation.neuronA], data.spike_detector.hist[options.histogram.binwidth][options.correlation.neuronB], 'valid'));

};

