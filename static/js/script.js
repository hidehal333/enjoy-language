const modalWrapper = document.querySelector('.modal-wrapper');
const images = document.getElementById('diarys');
const modalImage = document.querySelector('.modal-image');
console.log(images);

images.addEventListener("click", (event) => {
  if (event.target.classList.contains("image") === true ) {
    modalWrapper.classList.add('show');
    modalImage.classList.add('show');
    console.log(event.target.dataset);

    var imageSrc = event.target.dataset.src;
    modalImage.src = imageSrc;
  }
});

// モーダルを閉じる
modalWrapper.addEventListener('click', function() {
     if (this.classList.contains('show')) {
          this.classList.remove('show');
          modalImage.classList.remove('show');
     }
});
