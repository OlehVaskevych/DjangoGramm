export function initNavigation() {
    const $list = document.querySelectorAll('.nav-item');

    function activeLink() {
        $list.forEach(($li) => {
            $li.classList.remove('active');
        });
        this.classList.add('active');
    }

    $list.forEach(($li) => {
        $li.addEventListener('click', activeLink);
    });
}
