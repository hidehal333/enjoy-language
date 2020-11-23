const LikeButtons = document.getElementById('diarys');//いいねボタン

LikeButtons.addEventListener("click", (event) => {
  console.log(event.target);
  const div_liked = event.target.closest('#liked');
  print(div_liked)

  if (event.target.classList.contains("like") === true ) {
    event.preventDefault();

  var diary_id = event.target.getAttribute("value");
  console.log(diary_id);
    $.ajax({
        url: '{% url "diary:like" %}',
        type: 'POST',
        data: {
          'diary_id': diary_id,
          'csrfmiddlewaretoken': '{{ csrf_token }}'
        }
    //ajax成功
    }).done( response => {
      console.log(response);
        // HTMLを変更
        div_liked.innerHTML="OK"
          });
        };

});
