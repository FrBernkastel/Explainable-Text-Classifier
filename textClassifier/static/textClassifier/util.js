$(function () {
  $('[data-toggle="popover"]').popover()
})

$('.popover-dismiss').popover({
  trigger: 'focus'
})


$('body').on("keydown", "#input_text",function(e) {
    if (e.which == 13) {
      submitText();
    }
});

$('#input_text').each(function () {
  this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
}).on('input', function () {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
});


var maxLength=500;
function charLimit(el) {
    if (el.value.length > maxLength) return false;
    return true;
}
function characterCount(el) {
    var charCount = document.getElementById('charCount');
    if (el.value.length == 0) {
        $("#predict-id").parent().attr("disabled","disabled");
    }
    else {
      $("#predict-id").parent().removeAttr("disabled");
    }
    if (el.value.length > maxLength) el.value = el.value.substring(0,maxLength);
    if (charCount) charCount.innerHTML = maxLength - el.value.length;
    return true;
}

function clearText(el) {
  $('#input_text').val("");
  characterCount(el);
}

function fillbackTextArea(data) {
  $("#input_text").val(data["input_text"]);
}


//predict a text
function showAndPredict(data) {
  //1. fillback
  data_dict = {"input_text":data};
  fillbackTextArea(data_dict);

  //2. manual submitText
  submitText();
}

//utils for generate colorized sentences.
function textColor(color) {
  var color_class = "";
  if (color == 'green')
    color_class = "text-success";
  if (color == 'yellow')
    color_class = "text-warning";
  if (color == 'red')
    color_class = "text-danger";
  if (color == 'dark')
    color_class = "text-dark";
  if (color == 'white')
    color_class = "text-white";
  if (color == 'blue')
    color_class = "text-primary";
  return color_class
}

function labelTextColor(text, color) {
  //output: generate <span class='text-<color>'>text</span>
  var color_class = textColor(color);
  return "<span class = '%color_class%'>%text%</span>".replace("%color_class%",color_class).replace("%text%",text);
}


function findWordIndex(sent,word) {
  //core algorithm: very dirty work!
  res = new Array();
  var index = sent.indexOf(word);
  while(index >= 0) {
      var pre_flag = 1;
      var post_flag = 1;
      if (index > 0) {
        var preCh = sent[index-1];
        if (preCh>='a' && preCh <= 'z')
          pre_flag = 0;
      }
      if (index + word.length < sent.length) {
        var postCh = sent[index + word.length];
        if (postCh>='a' && postCh <= 'z')
          post_flag = 0;
      }
      if (pre_flag == 1 && post_flag == 1) {
        res.push(index);
      }
      index = sent.indexOf(word, index+1);
  }
  console.log(word, res.length);
  return res;
}

function generateColorSent(exp_words, input_text, color) {
    var i;
    var res_sent = input_text;
    for (i=0;i<exp_words.length;i++) {
      //algorithm to label the color of substring.
      var word = exp_words[i];
      var all_start_is = findWordIndex(res_sent.toLowerCase(), word);
      var text_blocks = new Array();
      var j;
      var prev_end_i = 0;
      for (j=0;j<all_start_is.length;j++) {
        var start_i = all_start_is[j];
        var end_i = start_i + word.length;
        var prev_text = res_sent.substring(prev_end_i,start_i);
        var text_to_color = res_sent.substring(start_i, end_i);
        text_blocks.push(prev_text);
        text_blocks.push(labelTextColor(text_to_color,color));
        prev_end_i = end_i;
      }
      text_blocks.push(res_sent.substring(prev_end_i,res_sent.length));
      res_sent = "";
      for (j=0;j<text_blocks.length;j++) {
        res_sent += text_blocks[j];
      }
    }
    return res_sent;
}


function beforeSubmitText() {
  $("#load-spinner").removeClass("d-none");
  $("#predict-id").addClass("d-none");
  $("#predict-id").parent().attr("disabled","disabled");
}

function afterSubmitText() {
  $("#load-spinner").addClass("d-none");
  $("#predict-id").removeClass("d-none");
  $("#predict-id").parent().removeClass("disabled");
  $("#predict-id").parent().removeAttr("disabled");
}