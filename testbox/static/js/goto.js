document.body.innerHTML += '<div style="position:absolute;bottom:0;right:0;margin:5px;-moz-border-radius:5px;-webkit-border-radius:5px;-webkit-border-radius:5px;">' +
    '<select style="width: auto;" id="id_where" onchange="goto(this.value)"></select>' +
    '</div>';

var URL = [
    ["BJ-boardfarm", "http://moon.ap.freescale.net/html/BJ-boardfarm"],
    ["BJ-boardfarm admin", "http://moon.ap.freescale.net/html/BJ-boardfarm/admin"],
    ["BJ-boardfarm logs", "http://moon.ap.freescale.net/html/BJ-boardfarm/logs"],
    ["bf-usage", "http://moon.ap.freescale.net/html/BJ-boardfarm/bf-usage.php"],
    ["ctrlpnl", "http://linux.freescale.net/scheduler/ctrlpnl.php"]
];

function goto(index) {
    window.location.href = URL[index][1];
}

window.onload = function () {
    var index = document.getElementById("id_goto").getAttribute("where");
    var where = document.getElementById("id_where");
    for (var i = 0; i < URL.length; i++) {
        where.options.add(new Option(URL[i][0], i, i==index, i==index));
    }
};
