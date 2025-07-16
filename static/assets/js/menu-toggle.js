document.addEventListener("DOMContentLoaded", function () {
  const navbarCollapse = document.querySelector('.navbar-collapse');

  document.querySelectorAll('.navbar-nav .nav-link').forEach(function (link) {
    link.addEventListener('click', function () {
      const isShown = navbarCollapse.classList.contains('show');
      if (isShown && !link.classList.contains('dropdown-toggle')) {
        new bootstrap.Collapse(navbarCollapse).hide();
      }
    });
  });
});
