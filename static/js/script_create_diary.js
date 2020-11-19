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

    $.ajax({
        'url': '{% url "diary:ajax_post_add" %}',
        'type': 'POST',
        'data': {
            'content': $('#id_content').val(),  // 記事タイトル
        },
        'dataType': 'json'
    }).done( response => {
        console.log(response);
        console.log(response.diary);
        console.log($('#diarys'));
        console.log($('#id_content'));
        // <p>はろー</p>のような要素を作成し、それを記事一覧エリアに追加し、入力欄をクリアする。
        // const p = $('<p>', {text: response.conent});
        const p =`
        <div class="card" >
          <!-- 投稿者の情報 -->
          ${ diary}
          ${diary.content}
          <div class="card-header bg-transparent border-bottom-0">
            <div class="row">
              <div class="col-auto">
                <a  href="{% url 'pages:profile' diary.user.pk %}">
                  {% if diary.user.profile_photo %}
                      <img class="rounded-circle" src="{{ diary.user.profile_photo.url }}" width="50" height="50"/>
                  {% endif %}
                </a>
              </div>
              <div class="col">
                <div class="row">
                  <div class="col-auto">
                    <b>{{ diary.user.nickname }}</b>
                  </div>
                  <div class="col">
                    <b>{{ diary.user.get_mother_language_display }}→{{ diary.user.get_learn_language_display }}</b>
                  </div>
                </div>
                <!-- 日記の更新日時 -->
                <div class="row">
                  <div class="col">
                    <small>{{ diary.updated_at }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="card-body">
            <!-- 日記のテキスト情報（タイトルはなし）　抜粋 -->
            <p class="card-text">{{ diary.content }}</p>
          </div>
          <!-- 日記写真（あれば表示、最大3） -->
          {% if diary.photo1 %}
            <div class="row text-center align-items-center px-1">
              <div class="col">
                <img src="{{ diary.photo1.url }}" class="img-fluid image" data-src="{{ diary.photo1.url }}"/>
              </div>
              {% if diary.photo2 %}
                <div class="col">
                  <img src="{{ diary.photo2.url }}" class="img-fluid image" data-src="{{ diary.photo2.url }}"/>
                </div>
                {% if diary.photo3 %}
                  <div class="col">
                    <img src="{{ diary.photo3.url }}" class="img-fluid image" data-src="{{ diary.photo3.url }}"/>
                  </div>
                {% endif %}
              {% endif %}
            </div>
          {% endif %}
          <!-- 日記リストフッター -->
          <div class="card-footer bg-transparent border-top-0">
            <div class="row justify-content-end">
              {% if request.user.id == diary.user.id %}
              <!-- 日記編集ボタン -->
              <div class="col-auto text-right align-items-center mt-3 mb-3">
                <a class="btn btn-success " href="{% url 'diary:diary_update' diary.pk %}">{% trans "編集" %}</a>
                <!-- 日記削除ボタン -->
                <button type="button" class="btn btn-danger delete-modal-button" data-toggle="modal" data-deleteurl="{% url 'diary:diary_delete' diary.pk %}" data-target="#modal_delete">
                  {% trans "削除" %}
                </button>
              </div>
              {% endif %}
            </div>
            <div class="row justify-content-start">
              <!-- いいね、コメント数 -->
              <div class="col-3">
              {% include 'diary/like.html' %}
              </div>
              <div class="col-3">
                <a class="btn btn-light border-secondary"  href="{% url 'comments:comments_create' diary.pk %}"  rel="nofollow" name="num_comment">{% trans "コメント" %} <span class="badge badge-light">{{ diary.comments.all|length}}</span></a>
              </div>
              <!-- 翻訳をする -->
              <div class="col">
              {% include 'diary/translate.html' %}
              </div>
            </div>
            <!-- コメントリスト -->
            {% if diary.comments.all %}
            <div class="row mt-2 py-2 border-top"　>
              コメント
            </div>
            {% endif %}
            {% for comment in diary.comments.all %}
            <div class="row pt-2">
              <!-- コメントユーザー写真 -->
              <div class="col-auto">
                <a href="{% url 'pages:profile' comment.user.pk %}">
                  {% if comment.user.profile_photo %}
                      <img class="rounded-circle" src="{{ comment.user.profile_photo.url }}" width="50" height="50"/>
                  {% endif %}
                </a>
              </div>
              <div class="col">
                <div class="row">
                  <div class="col-auto">
                    <b>{{ comment.user.nickname }}</b>
                  </div>
                  <!-- コメント日時 -->
                  <div class="col">
                    <small>{{ comment.created_at }}</small>
                  </div>
                  <!-- コメント削除 -->
                  <div class="col">
                    {% if request.user.id == comment.user.id %}
                      <button type="button" class="btn btn-danger py-2 px-3 delete-comment-modal-button" data-toggle="modal" data-deleteurl="{% url 'comments:comments_delete' comment.pk %}" data-target="#modal_delete_comment">
                        {% trans "削除" %}
                      </button>
                    {% endif %}
                  </div>
                </div>
              </div>
            </div>
            <div class="row border-bottom  pb-3">
              <div class="col" id="posts">
                <!-- コメントのテキスト情報　抜粋 -->
                <p>{{ comment.comment_content|truncatechars:300 }}</p>
              </div>
              <!-- コメント写真（あれば表示） -->
              {% if comment.photo %}
                <div class="row align-items-center px-1">
                  <div class="col">
                    <img src="{{ comment.photo.url }}" class="img-fluid image" data-src="{{ comment.photo.url }}" width="200" height="200"/>
                  </div>
                </div>
              {% endif %}
            </div>
          {% endfor %}
          </div>
        </div>
        `
        console.log(p);
        $('#diarys').prepend (p);
        $('#id_content').val('');
    });
});
