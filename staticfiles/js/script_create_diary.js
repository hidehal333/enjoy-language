$(document).on('change', ':file', function() {
    var input = $(this),
    numFiles = input.get(0).files ? input.get(0).files.length : 1,
    label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.parent().parent().next(':text').val(label);
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// 送信ボタンで呼ばれる
$('#ajax-add-post').on('submit', e => {
    // デフォルトのイベントをキャンセルし、ページ遷移しないように!
    e.preventDefault();

    let file1 = document.getElementById('input_image1').files[0];
    let file2 = document.getElementById('input_image2').files[0];
    let file3 = document.getElementById('input_image3').files[0];
    let content = document.getElementById('id_content').value;

    let fd = new FormData();
    fd.append('content', content);
    fd.append('image', file1);
    fd.append('image', file2);
    fd.append('image', file3);

    $.ajax({
        url: ajax_post_add_url,
        type: 'POST',
        // 'processData':false,
        // 'contentType':false,
        contentType : false,
        processData : false,
        data: fd,
        dataType: 'json'
    //ajax成功
    }).done( d => {
        // テンプレートに追加するhtmlタグを作成
        const p1 =`
        <div class="card" >
          <!-- 投稿者の情報 -->
          <div class="card-header bg-transparent border-bottom-0">
            <div class="row">
              <div class="col-auto">`;
                let profile_url = profile_url0.replace(0, d.user_id);

                if (d.photo_url) {
                  var p2 =`<a  href=${profile_url}>
                  <img class="rounded-circle" src="${d.photo_url}" width="50" height="50"/>
                  </a>`;
                  } else {
                  var p2 =  `<a  href=${profile_url}>
                            <img class="rounded-circle" src="" width="50" height="50"/>
                          </a>`;
                }

                const p3 =`</div>
                <div class="col">
                  <div class="row">
                    <div class="col-auto">
                      <b>${d.nickname}</b>
                    </div>
                    <div class="col">
                      <b>${d.mother_language }→${d.learn_language}</b>
                    </div>
                  </div>
                  <!-- 日記の更新日時 -->
                  <div class="row">
                    <div class="col">
                      <small>${d.created_at}</small>
                    </div>
                  </div>
                </div>
                </div>
                </div>
                <div class="card-body">
                <!-- 日記のテキスト情報（タイトルはなし）　抜粋 -->
                <p class="card-text">${d.content}</p>
                </div>`;

                // <!-- 日記写真（あれば表示、最大3） -->
if (d.photo1) {
var p4 = `<div class="row text-center align-items-center px-1">
                <div class="col">
                  <img src="${d.photo1}" class="img-fluid image" data-src="${d.photo1}"/>
                </div>`;
                if (d.photo2){
                  p4 += `<div class="col">
                                      <img src="${d.photo2}" class="img-fluid image" data-src="${d.photo2}"/>
                                    </div>`;
                                    if(d.photo3){
                                      p4 += `<div class="col">
                                                            <img src="${d.photo3}" class="img-fluid image" data-src="${d.photo3}"/>
                                                          </div>`;
                                    }
                }
          p4 +=`</div>`;
} else{
var p4 ="";
}

let diary_update_url = diary_update_url0.replace(/123456/, d.diary_id);
const diary_delete_url = diary_delete_url0.replace(/123456/, d.diary_id);
const p5 =`
          <!-- 日記リストフッター -->
          <div class="card-footer bg-transparent border-top-0">
            <div class="row justify-content-end">
              <!-- 日記編集ボタン -->
              <div class="col-auto text-right align-items-center mt-3 mb-3">
                <a class="btn btn-success " href=${diary_update_url}>{% trans "編集" %}</a>
                <!-- 日記削除ボタン -->
                <button type="button" class="btn btn-danger delete-modal-button" data-toggle="modal" data-deleteurl="${diary_delete_url}" data-target="#modal_delete">
                  {% trans "削除" %}
                </button>
              </div>
            </div>
            <div class="row justify-content-start">
`;

const p6 = `
<!-- いいね、コメント数 -->
<div class="col-3">
<form action="${like_url}" method="POST">
  {% csrf_token %}
   <!-- いいねをする -->
   <button type="submit"  name="diary_id" value="${d.diary_id}" class="btn btn-light border-secondary like">{% trans "いいね" %} <span class="badge badge-light">0</span></button>
</form>
</div>
`;

let comment_create_url = comment_create_url0.replace(/123456/, d.diary_id);

const p7 =`                <div class="col-3">
                <a class="btn btn-light border-secondary"  href=${comment_create_url}  rel="nofollow" name="num_comment">{% trans "コメント" %} <span class="badge badge-light">0</span></a>
              </div>

              <!-- 翻訳をする -->
              <div class="col">
                   <form action="${translate_url}" method="POST" target="_blank" name="form1">
                     {% csrf_token %}
                     <!-- 元の言語 -->
                     <!-- 翻訳する言語 -->
                      <!-- 翻訳をする -->
                      <button type="submit"  id="translate_${d.diary_id}" name="diary_id" value="${d.diary_id}" class="btn btn-light border-secondary translate">{% trans "日本語を英語に翻訳" %} </button>
                   </form>
              </div>
            </div>
          </div>
        </div>
        <hr>
`;

//各htmlを結合
const card_add = p1+p2+p3+p4+p5+p6+p7;

                // フォームを空白にする
                $('#diarys').prepend (card_add);
                $('#id_content').val('');
                $('#input_image1').val('');
                $('#input_image2').val('');
                $('#input_image3').val('');

            });
        });
