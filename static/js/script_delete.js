// <!-- 日記削除 -->
const deleteForm = document.getElementById('delete-form');
const deleteModalButtons = document.getElementsByClassName('delete-modal-button');

for (const button of deleteModalButtons) {
  button.addEventListener('click', () => {
  deleteForm.action = button.dataset.deleteurl;
  });
}

// <!-- コメント削除 -->
const deleteCommentForm = document.getElementById('delete-comment-form');
const deleteCommentModalButtons = document.getElementsByClassName('delete-comment-modal-button');

for (const button of deleteCommentModalButtons) {
  button.addEventListener('click', () => {
  deleteCommentForm.action = button.dataset.deleteurl;
  });
}
