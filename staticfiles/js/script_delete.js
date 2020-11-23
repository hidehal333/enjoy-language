// <!-- 日記削除 -->
const deleteModalButtons = document.getElementById('diarys');//日記一覧内
console.log(deleteModalButtons);
const deleteForm = document.getElementById('delete-form');//モーダル内


deleteModalButtons.addEventListener("click", (event) => {
    const modal = document.getElementById('modal_delete');//日記削除モーダル
    const diary_card = event.target.closest('.card');//イベントが発生した日記を取得

  if (event.target.classList.contains("delete-modal-button") === true ) {//日記内削除ボタン：イベントが発生した要素のクラスdelete-modal-buttonがあるならば
    const id = event.target.dataset.diary_id;

    deleteForm.addEventListener("click", (event) => {
      event.preventDefault();

    $.ajax({
        url: ajax_post_delete_url,
        type: 'POST',
        data:{
          diary_id: id
        }
    //ajax成功
    }).done( d => {
        // HTMLを変更
        //該当の投稿を削除
        diary_card.remove();
        //modalを非表示
        modal.classList.remove('show');
          });
        });
    };
});

// <!-- コメント削除 -->
const deleteCommentForm = document.getElementById('delete-comment-form');
const deleteCommentModalButtons = document.getElementsByClassName('delete-comment-modal-button');

for (const button of deleteCommentModalButtons) {
  button.addEventListener('click', () => {
  deleteCommentForm.action = button.dataset.deleteurl;
  });
}
