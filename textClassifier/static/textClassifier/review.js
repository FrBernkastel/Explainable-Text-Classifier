

function drawResult() {
    var pos_flag = $("#pos_paragraph").children(":first").text();
    var neg_flag = $("#neg_paragraph").children(":first").text();
    if (pos_flag == 1) {
      $("#pos_paragraph a").addClass("bg-success text-white");
      $("#pos_paragraph a").removeClass("btn-outline-dark");
      $("#neg_paragraph a").removeClass("bg-danger text-white");
      $("#neg_paragraph a").addClass("btn-outline-dark");
    } else if (neg_flag == 1) {
      $("#neg_paragraph a").addClass("bg-danger text-white");
      $("#neg_paragraph a").removeClass("btn-outline-dark");
      $("#pos_paragraph a").removeClass("bg-success text-white");
      $("#pos_paragraph a").addClass("btn-outline-dark");
    } else {
      $("#pos_paragraph a").removeClass("bg-success text-white");
      $("#pos_paragraph a").addClass("btn-outline-dark");
      $("#neg_paragraph a").removeClass("bg-danger text-white");
      $("#neg_paragraph a").addClass("btn-outline-dark");
    }
}

//onclick function, used for showing the toasts.
function toggleToast() {
  $("#toast-conclusion").toast("show");
  $("#toast-confidence").toast("show");
  $("#toast-explanation").toast("show");
}

//utility functions for label the text
function computeResult(data) {
  var pos_flag = data["pos_flag"];
  var neg_flag = data["neg_flag"];
  var res = "";
  var color = "";
  var prob = "50%";
  var prob_val = 50;

  if (pos_flag==0 && neg_flag==0) {
      res = "Neutral";
      color = "yellow";
  } else if (pos_flag == 1) {
      res = "Positive";
      color = "green";
      prob = data["pos_prob"].toFixed(2).toString() + "%";
      prob_val = data["pos_prob"];
  } else {
      res = "Negative";
      color = "red";
      prob = data["neg_prob"].toFixed(2).toString() + "%";
      prob_val = data["neg_prob"];
  }
  return {"text":res, "color":color, "prob":prob, "prob_val":prob_val};
}

//utility functions for submission
function switchResult(data) {
  $("#pos_paragraph").children(":first").text(data["pos_flag"]);
  $("#neg_paragraph").children(":first").text(data["neg_flag"]);
}

function computeProb(data) {
      var pos_prob = data["pos_prob"].toFixed(2);
      var neg_prob = data["neg_prob"].toFixed(2);
      percent_pos = pos_prob.toString() + "%";
      percent_neg = neg_prob.toString() + "%";
      $("#pos_bar").css("width",percent_pos);
      $("#neg_bar").css("width",percent_neg);
      $("#pos_paragraph a").attr("data-content",percent_pos);
      $("#neg_paragraph a").attr("data-content",percent_neg);
      $("#pos_paragraph a").popover("show");
      $("#neg_paragraph a").popover("show");
}

function procConclusionToast(data) {
  res = computeResult(data);
  text = res["text"];
  color = res["color"];
  var res_sent = "<h6> The review is " + labelTextColor(text, color)+" .</h6>";
  $("#toast-conclusion .toast-body").html(res_sent);
  $("#toast-conclusion .toast-header i").removeClass("text-success text-warning text-danger").addClass(textColor(color));
  $("#toast-conclusion").toast("show");
}

function procProbabilityToast(data) {
  res = computeResult(data);
  prob = res["prob"];
  color = res["color"];
  prob_val = res["prob_val"];

  if (prob_val !== 50) {
      var res_sent = "<h6> The probability is " + labelTextColor(prob, color) + ".</h6>";

      $("#toast-probability .toast-body").html(res_sent);
      $("#toast-probability .toast-header i").removeClass("text-success text-warning text-danger").addClass(textColor(color));
      $("#toast-probability").toast("show");
  } else {
      $("#toast-probability").toast("hide");
  }
}

function procConfidenceToast(data) {
  res = computeResult(data);
  prob_val = res["prob_val"];

  var res_sent;

  if (prob_val === 50) {
      res_sent = "<h6>This is an emotionless sentence.</h6>";
  }

  if (prob_val < 70 && prob_val > 50) {
      res_sent = "<h6>We are not very confident about this prediction.</h6>";
  }
  if (prob_val < 90 && prob_val >=70) {
      res_sent = "<h6>We are confident about this prediction.</h6>";
  }
  if (prob_val >= 90) {
      res_sent = "<h6>We are very certain about this prediction.</h6>";
  }

  $("#toast-confidence .toast-body").html(res_sent);
  $("#toast-confidence .toast-header i").removeClass("text-success text-warning text-danger").addClass(textColor(color));
  $("#toast-confidence").toast("show");
}

function procExplanationToast(data) {
  exp_words = data["exp_words"];
  res = computeResult(data);
  color = res["color"];
  text = res["text"];
  var res_sent = "";
  if (text == "Neutral") {
    res_sent = "This sentence doesn't make any sense!";
  } else {
    res_sent = data["input_text"];
    res_sent = generateColorSent(exp_words, res_sent, color);
  }
  $("#toast-explanation .toast-body").html("<h6>"+res_sent+"</h6>");
  $("#toast-explanation .toast-header i").removeClass("text-success text-warning text-danger").addClass(textColor(color));
  $("#toast-explanation").toast("show");
}

//submission code
function submitText() {
  var text = $('#input_text').val();
  console.log("Enter review.js submitText()")
  beforeSubmitText();

  $.ajax({
    type: "POST",
    url: "predict/",
    data: {"input_text":text},
    dataType: "json",
    success: function (data) {
      console.log('Submission was successful.');
      $('#explanation').text(data["explanation"]); //experimental
      switchResult(data);
      fillbackTextArea(data);
      computeProb(data);
      afterSubmitText();
      procConclusionToast(data);
      procProbabilityToast(data);
      procConfidenceToast(data);
      procExplanationToast(data);
      drawResult();
    },
    error: function (data) {
      console.log('An error occurred in submitText(). (review.js)');
      console.log(data);
      afterSubmitText();

    },
  });

}

//random pick and predict
function randomPredict() {
    $.ajax({
        type: "GET",
        url: "pick/",
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
