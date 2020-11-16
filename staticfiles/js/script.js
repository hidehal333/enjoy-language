const modalWrapper = document.querySelector('.modal-wrapper');
const images = document.querySelectorAll('.image');
const modalImage = document.querySelector('.modal-image');
console.log(images);

images.forEach(function(image, index) {
     image.onclick = function() {
          modalWrapper.classList.add('show');
          modalImage.classList.add('show');
          console.log(this.dataset);

          var imageSrc = this.dataset.src;
          modalImage.src = imageSrc;
     };
});
// モーダルを閉じる
modalWrapper.addEventListener('click', function() {
     if (this.classList.contains('show')) {
          this.classList.remove('show');
          modalImage.classList.remove('show');
     }
});
