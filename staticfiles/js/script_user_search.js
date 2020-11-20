
  const button_all = document.getElementById('ajax-user_search_all');
  const button_mother = document.getElementById('ajax-user_search_mother');
  const button_learn = document.getElementById('ajax-user_search_learn');

  //ユーザー検索（すべてのユーザー）
  // 送信ボタンで呼ばれる
  $('#ajax-user_search_all').click(function(e) {
  // デフォルトのイベントをキャンセルし、ページ遷移しないように!
    e.preventDefault();
    button_all.className = "btn btn-dark border-secondary";
    button_mother.className = "btn btn-light border-secondary";
    button_learn.className = "btn btn-light border-secondary";

    $.ajax({
        'url': ajax_usersearchall_url,
        'type': 'GET',
    }).done( response => {
      // 記事欄を真っ白にする。
      $('#user_search').empty();

      for (const user of response.user_list) {
        // htmlを追加
        // もし写真があるならば写真追加
        let profile_url = profile_url0.replace(0, user.id);
        if(user.profile_photo_url) {
          const user_list = `
            <div class="info">
            <a  href=${profile_url}>
                  <img src="${user.profile_photo_url}" width="50" height="50">  ${user.name}  ${user.ange}  ${user.mother_language}→${user.learn_language}
            </a>
            </div>
            <hr>`;
            $('#user_search').append(user_list);
        }
        else {
          const user_list = `
          <div class="info">
              <a  href=${profile_url}>
                 ${user.name}  ${user.ange}  ${user.mother_language}→${user.learn_language}
              </a>
          </div>
          `;
          $('#user_search').append(user_list);
        }

      }
    });
  });

  //ユーザー検索（学習を手伝う：母語＝学習言語）
  // 送信ボタンで呼ばれる
  $('#ajax-user_search_mother').click(function(e) {
    // デフォルトのイベントをキャンセルし、ページ遷移しないように!
    e.preventDefault();
    button_mother.className = "btn btn-dark border-secondary";
    button_all.className = "btn btn-light border-secondary";
    button_learn.className = "btn btn-light border-secondary";

    $.ajax({
        'url': ajax_usersearchmother_url,
        'type': 'GET',
    }).done( response => {
      // 記事欄を真っ白にする。
      $('#user_search').empty();

     for (const user of response.user_list) {
       // htmlを追加
       // もし写真があるならば写真追加
       let profile_url = profile_url0.replace(0, user.id);
       if(user.profile_photo_url) {
         const user_list = `
           <div class="info">
           <a  href=${profile_url}>
                 <img src="${user.profile_photo_url}" width="50" height="50">  ${user.name}  ${user.ange}  ${user.mother_language}→${user.learn_language}
           </a>
           </div>
           <hr>`;
           $('#user_search').append(user_list);
       }
       else {
         const user_list = `
         <div class="info">
             <a  href=${profile_url}>
                ${user.name}  ${user.ange}  ${user.mother_language}→${user.learn_language}
             </a>
         </div>
         `;
         $('#user_search').append(user_list);
        }
      }
    });
  });

  //ユーザー検索（学習仲間：学習言語＝学習言語）
  // 送信ボタンで呼ばれる
  $('#ajax-user_search_learn').click(function(e) {
      // デフォルトのイベントをキャンセルし、ページ遷移しないように!
      e.preventDefault();
      button_learn.className = "btn btn-dark border-secondary";
      button_all.className = "btn btn-light border-secondary";
      button_mother.className = "btn btn-light border-secondary";

      $.ajax({
          'url': ajax_usersearchlearn_url,
          'type': 'GET',
      }).done( response => {
        // 記事欄を真っ白にする。
        $('#user_search').empty();

     for (const user of response.user_list) {
       // htmlを追加
       // もし写真があるならば写真追加
       let profile_url = profile_url0.replace(0, user.id);
       if(user.profile_photo_url) {
         const user_list = `
           <div class="info">
           <a  href=${profile_url}>
                 <img src="${user.profile_photo_url}" width="50" height="50">  ${user.name}  ${user.ange}  ${user.mother_language}→${user.learn_language}
           </a>
           </div>
           <hr>`;
           $('#user_search').append(user_list);
       }
       else {
         const user_list = `
         <div class="info">
             <a  href=${profile_url}>
                ${user.name}  ${user.ange}  ${user.mother_language}→${user.learn_language}
             </a>
         </div>
         `;
         $('#user_search').append(user_list);
        }
      }
    });
  });
