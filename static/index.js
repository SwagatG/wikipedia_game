$(function() {
    $("#submit_game").bind('click', function(e) {
        e.preventDefault();
        console.log(document.getElementById("chart"));
        document.getElementById("chart").style.display = "block";
        document.getElementById("start_form").style.display = "none";

        $.ajax({
            type: "POST",
            url: "/start_computation",
            data: $('#wikiGameForm').serialize(),
            // data: {
            //  start_page: ("#start_page").val(),
            //  end_page: ("#end_page").val(),
            //  max_turns: ("#max_turns").val()
            // },
            success: function(data) {
              data = JSON.parse(data);
                try {
                    if (data['errors'] != false) {
                        if (data['errors'] == true) {
                            alert("There was an unknown error.")
                        } else if (data['errors'].length == 1) {
                            alert(data['errors'][0] + " is not a valid Wikipedia page name.")
                        } else {
                            alert(data['errors'][0] + " and " + data['errors'][1] + " are not a valid Wikipedia page names.")
                        }
                    } else {
                        generateGraph();
                    }
                } catch (err) {
                    alert("There was an unknown error: " + err);
                }

            },
            error: function(data) {
                alert("ERROR: " + str(data));
            }
        });
    });
});

function generateGraph() {
    $.ajax({
        type: "GET",
        url: "/get_status",

        success: function(data) {
          // alert(data);
          
          data = JSON.parse(data);
          // alert(data["path"]);

            labels = [];
            values = [];
            var max_score = 0;

            for (var i = 0; i < data["path"].length; ++i) {
              labels.push(data["path"][i]["title"]);
              //labels.push(i);
                values.push(data["path"][i]["score"]);
                if (data["path"][i]["score"] > max_score) {
                    max_score = data["path"][i]["score"];
                }
            }
            
            // alert(max_score);

            for (var i = 0; i < values.length; ++i) {
                values[i] = values[i] / max_score * 100;
            }
            // alert(values.String)

            var barData = {
                labels: labels,
                datasets: [{
                    fillColor: "rgba(151,187,205,0.2)",
                    strokeColor: "rgba(151,187,205,1)",
                    pointColor: "rgba(151,187,205,1)",
                    pointStrokeColor: "#fff",
                    pointHighlightFill: "#fff",
                    pointHighlightStroke: "rgba(151,187,205,1)",
                    bezierCurve: false,
                    data: values
                }]
            }

            console.log(labels);
            console.log(values);

            Chart.defaults.global.animationSteps = 50;
            Chart.defaults.global.tooltipYPadding = 16;
            Chart.defaults.global.tooltipCornerRadius = 0;
            Chart.defaults.global.tooltipTitleFontStyle = "normal";
            Chart.defaults.global.tooltipFillColor = "rgba(0,0,0,0.8)";
            Chart.defaults.global.animationEasing = "easeOutBounce";
            Chart.defaults.global.responsive = false;
            Chart.defaults.global.scaleLineColor = "black";
            Chart.defaults.global.scaleFontSize = 10;

            // get bar chart canvas
            var mychart = document.getElementById("chart").getContext("2d");

            steps = 10
            max = 100
            // draw bar chart
            var LineChartDemo = new Chart(mychart).Line(barData, {
                scaleOverride: true,
                scaleSteps: steps,
                scaleStepWidth: Math.ceil(max / steps),
                scaleStartValue: 0,
                scaleShowVerticalLines: true,
                scaleShowGridLines: true,
                barShowStroke: true,
                scaleShowLabels: true,
                bezierCurve: true,
                options:
                {
                    scales:
                    {
                        xAxes: [{
                            display: false
                        }]
                    }
                }
                // showXAxisLabel: false,
                // opt33asdfdfasdfasdasdf

            });

            if (data["complete"] == false) {
              generateGraph();
            }
        }
    });
}