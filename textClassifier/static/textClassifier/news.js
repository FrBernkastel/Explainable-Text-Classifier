function drawResult(data) {
    var labels = data['labels'];
    $.each(labels, function(idx, l) {
        var badge = $('#label'+idx);
        badge.text(l[0]);
        badge.removeClass('d-none');
    });
}

function procConclusionToast(data) {
  var res = "POLITICS";
  var res_sent = "The label is %res%.".replace("%res%",res);
  console.log(res_sent);
  $("#toast-conclusion .toast-body").text(res_sent);
  $("#toast-conclusion").toast("show");
}

probab_data = {
    datasets: [{
        data: [1,2,3,4,5,
        1,2,3,4,5,
        1,2,3,4,5,
        1,2,3,4,5,
        1,2,3,4,5,6,
        1,2,3,4,5,],
        backgroundColor:
            ['rgba(255,0,0,1)', 'rgba(255,99,71,1)', 'rgba(255,127,80,1)', 'rgba(250,128,114,1)', 'rgba(255,165,0,1)',
            'rgba(255,215,0,1)', 'rgba(218,165,32,1)', 'rgba(189,183,107,1)', 'rgba(128,128,0,1)', 'rgba(255,255,0,1)',
            'rgba(154,205,50)', 'rgba(107,142,35)', 'rgba(127,255,0,1)', 'rgba(50,205,50,1)', 'rgba(152,251,152,1)',
            'rgba(102,205,170,1)', 'rgba(0,255,255,1)', 'rgba(64,224,208,1)', 'rgba(175,238,238)', 'rgba(95,158,160,1)',
            'rgba(100,149,237)', 'rgba(0,191,255)', 'rgba(135,206,235,1)', 'rgba(0,0,128,0.8)', 'rgba(65,105,225,1)', 'rgba(138,43,226,1)',
            'rgba(106,90,205,1)', 'rgba(128,0,128,1)', 'rgba(219,112,147,1)', 'rgba(255,192,203,1)', 'rgba(210,105,30,1)',
            // {#"tomato", "dark salmon", "salmon", "dark orange",#}
            // {#"gold", "golden rod", "dark khaki", "olive", "yellow",#}
            // {#"yellow green", "olive drab", "chart reuse", "dark green", "sea green",#}
            // {#"medium aqua marine", "aqua", "turquoise", "pale turquoise", "cadet blue",#}
            // {#"corn flower blue", "deep sky blue", "sky blue", "navy", "royal blue", "blue violet",#}
            // {#"slate blue", "purple", "pale violet red", "pink", "saddle brown"#}
        ]
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: ['ARTS', 'ARTS & CULTURE', 'BLACK VOICES', 'BUSINESS', 'COLLEGE',
       'COMEDY', 'CRIME', 'EDUCATION', 'ENTERTAINMENT', 'FIFTY',
       'GOOD NEWS', 'GREEN', 'HEALTHY LIVING', 'IMPACT', 'LATINO VOICES',
       'MEDIA', 'PARENTS', 'POLITICS', 'QUEER VOICES', 'RELIGION',
       'SCIENCE', 'SPORTS', 'STYLE', 'TASTE', 'TECH', 'THE WORLDPOST',
       'TRAVEL', 'WEIRD NEWS', 'WOMEN', 'WORLD NEWS', 'WORLDPOST'],

};

function procPieChartsToast(data) {
    $('#myChart').remove();
    $('#chart-container').append('<canvas id="myChart" width="1200" height="600"></canvas>');
    probab_data.datasets[0].data = data['prob'];
    var ctx =$('#myChart');
    var myPieChart = new Chart(ctx, {
        type: 'doughnut',
        data: probab_data,
        options: {
          // {#responsive: false,#}
          legend: {
             display: false,
             position: 'bottom',
             fontSize: 3,
             // {#onClick: null#}
          },
          title: {
            display: true,
            text: 'Predicted probabilities of each category'
          }
        }

    });
    $('#toast-chart').toast("show");
}

//submission code
function submitText(){
    //3. remove example
  $("#news-example").remove();
  $("#example-text").remove();
  if ($("#input_text").val().length == 0) {
  }

  else {
      var text = $('#input_text').val();

      $.ajax({
        type: "POST",
        url: "../predict2/",
        data: {"input_text":text},
        dataType: "json",
        success: function (data) {
          console.log('Submission was successful.');
          console.log(data["input_text"]);
          $('#explanation').text(data["explanation"]); //experimental
          fillbackTextArea(data);

          drawResult(data);
          procConclusionToast(data);
          procPieChartsToast(data);

        },
        error: function (data) {
          console.log('An error occurred.');
          console.log(data);
        },
      });
  }
}

//show default example
function showExample() {
  
  //1. fillback
  //2. manual submitText
  var input_text = $("#example-text h6").text();
  showAndPredict(input_text);

  //3. remove example
  $("#news-example").remove();
  $("#example-text").remove();
}

//random pick and predict
function randomPredict_news() {
    $.ajax({
        type: "GET",
        url: "../pick2/",
        success: function (data) {
            showAndPredict(data);
        },
        error: function (data) {
            console.log('An error occurred in randomPick(). (review.js)');
            console.log(data);
        }
    });
}