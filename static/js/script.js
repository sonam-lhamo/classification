// document.getElementById('toggleNavbar').addEventListener('click', function() {
//     document.getElementById('navbar').style.display = 'block';
//     document.querySelector('.overlay').style.display = 'none';
//   });
  
//   document.getElementById('closeNavbar').addEventListener('click', function() {
//     document.getElementById('navbar').style.display = 'none';
//     document.querySelector('.overlay').style.display = 'block';
//   });


document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('toggleNavbar').addEventListener('click', function() {
      document.getElementById('navbar').style.display = 'block';
      if (window.innerWidth < 431) {
          document.querySelector('.overlay').style.display = 'none';
      }
  });

  document.getElementById('closeNavbar').addEventListener('click', function() {
      document.getElementById('navbar').style.display = 'none';
      if (window.innerWidth < 431) {
          document.querySelector('.overlay').style.display = 'block';
      }
  });
});
