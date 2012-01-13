function prep_vis() {

    /* Tile the visualization for each job. */
    var vis = new pv.Panel()
        .data(data)
        .width(w)
        .height(h + 10)
        .top(6)
        .left(6)
        .right(6)
        .bottom(6)
        .canvas(function(d) d.status[0]["id"].toString());

    /* A panel instance to store scales (x, y) and the mouseover index (i). */
    var panel = vis.add(pv.Panel)
        .def("i", -1)
        .def("x", function(d) pv.Scale.linear(d.values, pv.index).range(0, w))
        .def("y", function(d) pv.Scale.linear(pv.min(d.values), pv.max(d.values)).range(0, h))
        .bottom(10)
        .events("all")
        .event("mousemove", pv.Behavior.point(Infinity).collapse("y")); 

    /* The line. */
    panel.add(pv.Line)
        .data(function(d) d.values)
        .left(function() panel.x()(this.index))
        .bottom(function(d) panel.y()(d))
        .event("point", function() panel.i(this.index))
        .event("unpoint", function() panel.i(-1));

    /* The x-axis. */
    panel.add(pv.Rule)
        .bottom(0);

    /* The mouseover dot. */
    panel.add(pv.Dot)
        .visible(function() panel.i() >= 0)
        .left(function() panel.x()(panel.i()))
        .bottom(function(d) panel.y()(d.values[panel.i()]))
        .fillStyle("#ff7f0e")
        .strokeStyle(null)
        .size(10);

    /* The label: either the job name, or the value. */
    panel.add(pv.Label)
        .bottom(-1)
        .textBaseline("top")
        .left(function() panel.i() < 0 ? 0 : null)
        .right(function() panel.i() < 0 ? null : 0)
        .textAlign(function() panel.i() < 0 ? "left" : "right")
        .textStyle(function() panel.i() < 0 ? "#999" : "#000")
        .text(function(d) panel.i() < 0 ? "Neuron ["+ d.status[0]["id"] +"]"
            : times[panel.i()] + " ms: "+ numberFormat(d.values[panel.i()]) + " mV");

    return vis;

}