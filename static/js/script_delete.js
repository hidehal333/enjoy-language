// <!-- 日記削除 -->
const deleteForm = document.getElementById('delete-form');//モーダル内
const deleteModalButtons = document.getElementById('diarys');//日記一覧内


deleteModalButtons.addEventListener("click", (event) => {
  if (event.target.classList.contains("delete-modal-button") === true ) {
    deleteForm.action = event.target.dataset.deleteurl;
  }
});

// <!-- コメント削除 -->
const deleteCommentForm = document.getElementById('delete-comment-form');
const deleteCommentModalButtons = document.getElementsByClassName('delete-comment-modal-button');

for (const button of deleteCommentModalButtons) {
  button.addEventListener('click', () => {
  deleteCommentForm.action = button.dataset.deleteurl;
  });
}
