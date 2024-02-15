function movePdocNavBar(e) {
    navbar = document.querySelector('nav.pdoc');
    navbar.querySelector('.memberlist').classList.add('md-nav__list');
    navbar.querySelectorAll('.memberlist a').forEach(a => a.classList.add('md-nav__link'));

    sidebar = document.querySelector('.md-sidebar--secondary .md-sidebar__inner')
    sidebar.innerHTML = navbar.outerHTML;
    navbar.remove();
}
document.addEventListener("DOMContentLoaded", movePdocNavBar);
