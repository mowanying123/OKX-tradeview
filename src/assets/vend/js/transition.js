document.addEventListener('DOMContentLoaded', function() {
    const navButtons = document.querySelectorAll('.nav-button');
    
    navButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const direction = this.classList.contains('next') ? 'right' : 'left';
            const currentPage = document.querySelector('.current-page');
            const nextPageUrl = this.dataset.href;

            // 添加滑出动画类
            currentPage.classList.add(`slide-${direction}`);

            // 在动画结束后加载新页面
            currentPage.addEventListener('transitionend', function loadNewPage() {
                window.location.href = nextPageUrl;
                currentPage.removeEventListener('transitionend', loadNewPage);
            });
        });
    });
});