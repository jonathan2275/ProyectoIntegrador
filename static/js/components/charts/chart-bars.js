//
// Bars chart
//

var BarsChart = (function() {

    //
    // Variables
    //

    var $chart = $('#chart-bars');


    //
    // Methods
    //

    // Init chart
    function initChart($chart) {
        let label = [];
        let value = [];
        $.ajax({
            url: "/MostSeller",
            type: 'GET',
            success: function(resp) {
                resp.produ.forEach(element => {
                    label.push(element[1]);
                    value.push(element[0]);
                });

            },
            error: function(err) {
                console.log(err);
            }
        });

        // Create chart
        var ordersChart = new Chart($chart, {
            type: 'bar',
            data: {
                labels: label,
                datasets: [{
                    label: 'vendidos',
                    data: value
                }]
            }
        });

        // Save to jQuery object
        $chart.data('chart', ordersChart);
    }


    // Init chart
    if ($chart.length) {
        initChart($chart);
    }

})();