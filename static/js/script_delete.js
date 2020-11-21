// <!-- 日記削除 -->
const deleteForm = document.getElementById('delete-form');//モーダル内
const deleteModalButtons = document.getElementById('diarys');//日記一覧内


deleteModalButtons.addEventListener("click", (event) => {
    const modal = document.getElementById('modal_delete');
    const diary_card = event.target.closest('.card');

  if (event.target.classList.contains("delete-modal-button") === true ) {
    const id = event.target.dataset.diary_id;
    console.log(id);

    deleteForm.addEventListener("click", (event) => {
      event.preventDefault();
      console.log(event);

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
