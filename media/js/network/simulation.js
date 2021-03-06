function connect_to_output(element, index, array) {
    return (element.source.type == 'output' || element.target.type == 'output')
}

function connect_to_input(element, index, array) {
    return (element.source.type == 'input' || element.target.type == 'input')
}

// LOOPING REQUEST FOR SIMULATION PROGRESS
function check_task_status(task_id) {
    $.getJSON('/status/'+task_id+'/?', function(data) {
            var task = data['task'];
            var status = task['status'];

            show_msg('Simulation info', 'Simulation is running.<p>Loading... please wait.</p>', 'pending')
            $( "#dialog-msg #task_status" ).html(status);

            if (status == 'PENDING') {
                window.setTimeout(function() {check_task_status(task_id)}, 2000);
            } else {
                if (status == 'ABORTED') {
                    alert(task_status)
                } else if (status == 'FAILURE') {
                    alert(task_status)
                }

                window.setTimeout(function() {
                    result = task['result']
                    window.location.href = '/network/'+ SPIC_group + '/' + SPIC_local_id + '/' + result['local_id'];
                }, 1000);
            }
    });
};

function simulate() {
    var clean_nodes = nodes.map(function (n) {
        return {
            uid: n.uid, id: n.id,
            label: n.label, type: n.type,
            synapse: n.synapse,
            status: n.status, disabled: n.disabled,
            x: n.x/options.layout.width,
            y: n.y/options.layout.height}
        })

    var clean_links = links.map(function (l) {
        return {
            source: l.source.uid, target: l.target.uid,
            weight: l.weight, delay: l.delay}
        })

    $( "#network-form" ).find("#id_nodes").val(JSON.stringify(clean_nodes));
    $( "#network-form" ).find("#id_links").val(JSON.stringify(clean_links));

    var form = $( "#network-form" ).serialize();
    $( ":input" ).attr("disabled", true);

    $.post('/network/ajax/'+ network_id +'/simulate/',
        form,
        function(task_id){
            check_task_status(task_id);
    });
};
