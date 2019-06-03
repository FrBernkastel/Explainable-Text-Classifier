var background_color_dict = {
    'ARTS': 'rgba(255,0,0,1)', 'ARTS & CULTURE': 'rgba(255,99,71,1)', 'BLACK VOICES': 'rgba(255,127,80,1)',
    'BUSINESS': 'rgba(250,128,114,1)', 'COLLEGE': 'rgba(255,165,0,1)', 'COMEDY': 'rgba(255,215,0,1)',
    'CRIME': 'rgba(218,165,32,1)', 'EDUCATION': 'rgba(189,183,107,1)', 'ENTERTAINMENT': 'rgba(128,128,0,1)',
    'FIFTY': 'rgba(255,255,0,1)', 'GOOD NEWS': 'rgba(154,205,50)', 'GREEN': 'rgba(107,142,35)',
    'HEALTHY LIVING': 'rgba(127,255,0,1)', 'IMPACT': 'rgba(50,205,50,1)', 'LATINO VOICES': 'rgba(152,251,152,1)',
    'MEDIA': 'rgba(102,205,170,1)', 'PARENTS': 'rgba(0,255,255,1)', 'POLITICS': 'rgba(64,224,208,1)',
    'QUEER VOICES': 'rgba(175,238,238)', 'RELIGION': 'rgba(95,158,160,1)', 'SCIENCE': 'rgba(100,149,237)',
    'SPORTS': 'rgba(0,191,255)', 'STYLE': 'rgba(135,206,235,1)', 'TASTE': 'rgba(0,0,128,0.8)',
    'TECH': 'rgba(65,105,225,1)', 'THE WORLDPOST': 'rgba(138,43,226,1)', 'TRAVEL': 'rgba(106,90,205,1)',
    'WEIRD NEWS': 'rgba(128,0,128,1)', 'WOMEN': 'rgba(219,112,147,1)', 'WORLD NEWS': 'rgba(255,192,203,1)',
    'WORLDPOST': 'rgba(210,105,30,1)'};

var color_dict = {'ARTS': 'white', 'ARTS & CULTURE': 'black', 'BLACK VOICES': 'black', 'BUSINESS': 'black',
    'COLLEGE': 'black', 'COMEDY': 'black', 'CRIME': 'black', 'EDUCATION': 'black', 'ENTERTAINMENT': 'white',
    'FIFTY': 'black', 'GOOD NEWS': 'black', 'GREEN': 'white', 'HEALTHY LIVING': 'black', 'IMPACT': 'black',
    'LATINO VOICES': 'black', 'MEDIA': 'black', 'PARENTS': 'black', 'POLITICS': 'black', 'QUEER VOICES': 'black',
    'RELIGION': 'white', 'SCIENCE': 'black', 'SPORTS': 'black', 'STYLE': 'black', 'TASTE': 'white', 'TECH': 'white',
    'THE WORLDPOST': 'white', 'TRAVEL': 'black', 'WEIRD NEWS': 'white', 'WOMEN': 'white', 'WORLD NEWS': 'black',
    'WORLDPOST': 'black'};

var color_contract_dict = {'rgba(255,0,0,1)': 'white', 'rgba(255,99,71,1)': 'black', 'rgba(255,127,80,1)':
        'black', 'rgba(250,128,114,1)': 'black', 'rgba(255,165,0,1)': 'black', 'rgba(255,215,0,1)': 'black',
    'rgba(218,165,32,1)': 'black', 'rgba(189,183,107,1)': 'black', 'rgba(128,128,0,1)': 'white',
    'rgba(255,255,0,1)': 'black', 'rgba(154,205,50)': 'black', 'rgba(107,142,35)': 'white',
    'rgba(127,255,0,1)': 'black', 'rgba(50,205,50,1)': 'black', 'rgba(152,251,152,1)': 'black',
    'rgba(102,205,170,1)': 'black', 'rgba(0,255,255,1)': 'black', 'rgba(64,224,208,1)': 'black',
    'rgba(175,238,238)': 'black', 'rgba(95,158,160,1)': 'white', 'rgba(100,149,237)': 'black',
    'rgba(0,191,255)': 'black', 'rgba(135,206,235,1)': 'black', 'rgba(0,0,128,0.8)': 'white',
    'rgba(65,105,225,1)': 'white', 'rgba(138,43,226,1)': 'white', 'rgba(106,90,205,1)': 'black',
    'rgba(128,0,128,1)': 'white', 'rgba(219,112,147,1)': 'white', 'rgba(255,192,203,1)': 'black',
    'rgba(210,105,30,1)': 'black'};


function drawResult(data) {
    var labels = data['labels'];
    var start = 0;
    $.each(labels, function(idx, l) {
        console.log(idx);
        var badge = $('#label'+idx);

        badge.css({"background-color":background_color_dict[l[0]], color:color_dict[l[0]]});
        badge.text(l[0]);
        badge.removeClass('d-none');
        start = idx+1;
    });

    for (;start<5;start++) {
        var badge = $('#label'+start);
        badge.addClass('d-none');
    }
}

function procExpToast(data) {
  var flag = data['flag'];
  var exp = data['explanation'];
  var input_text = data['input_text'];
  var top1 = data['labels'][0][0]
  var exp_words_prob = exp[top1];
  var i;
  var exp_words = []
  for (i=0;i<exp_words_prob.length;i++) {
      exp_words.push(exp_words_prob[i][0]);
  }
  //get exp_words
  var res_sent = "";
  if (flag != true) {
    res_sent = "It's a meaningless sentence!";
  }
  else if(exp_words.length==0) {
    res_sent = "This sentence can't be categorized";
  } else {
    var color = background_color_dict[top1];
    var res_sent = generateColorSent(exp_words, input_text, color, false);
  }
  $("#toast-explanation .toast-body").html("<h6>"+res_sent+"</h6>");
  $("#toast-explanation").toast("show");
}

function procConclusionToast(data) {
  var res = "POLITICS";
  var res_sent = "The label is %res%.".replace("%res%",res);
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
            text: 'Predicted probabilities of each category',
            fontSize: 14,
          }
        }

    });
    $('#toast-chart').toast("show");
}

//submission code
function submitText(){
    //3. remove example
  $("#news-example").remove();
  $("#chart-container").removeClass("d-none");
  beforeSubmitText();
  console.log("enter news.js submitText()");

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
          $('#explanation').text(data["explanation"]); //experimental
          fillbackTextArea(data);
          drawResult(data);
          afterSubmitText();
          procExpToast(data);
          procPieChartsToast(data);
        },
        error: function (data) {
          afterSubmitText();
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
            characterCount($("textarea")[0]);
        },
        error: function (data) {
            console.log('An error occurred in randomPick(). (review.js)');
            console.log(data);
        }
    });
}