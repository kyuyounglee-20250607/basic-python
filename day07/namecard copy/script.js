// 온라인 명함 사이트 JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('온라인 명함 사이트가 로드되었습니다.');
    
    // 여기에 추가적인 기능을 구현할 수 있습니다
    // 예: 애니메이션, 인터랙션 등

    const tabs = ['main', 'detail', 'share'];
    const showTab = (tab) => {
        tabs.forEach(t => {
            const el = document.getElementById('tab-' + t);
            if (el) {
                el.classList.toggle('d-none', t !== tab);
                el.classList.toggle('block', t === tab);
            }
        });
    };
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            showTab(this.dataset.tab);
        });
    });
    // 상세페이지 ← 버튼: 메인으로
    const detailBackBtn = document.querySelector('#tab-detail button[title="Back"]');
    if (detailBackBtn) {
        detailBackBtn.addEventListener('click', function() {
            showTab('main');
        });
    }
    // 상세페이지 공유 버튼: 공유로
    const detailShareBtn = document.querySelector('#tab-detail button[title="Share"]');
    if (detailShareBtn) {
        detailShareBtn.addEventListener('click', function() {
            showTab('share');
        });
    }
    // 공유페이지 X 버튼: 메인으로
    const shareCloseBtn = document.querySelector('#tab-share button[title="Close"]');
    if (shareCloseBtn) {
        shareCloseBtn.addEventListener('click', function() {
            showTab('main');
        });
    }
    showTab('main');
}); 