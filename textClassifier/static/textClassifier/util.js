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
