// 온라인 명함 사이트 JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('온라인 명함 사이트가 로드되었습니다.');
    
    // 여기에 추가적인 기능을 구현할 수 있습니다
    // 예: 애니메이션, 인터랙션 등

    const tabs = ['main', 'detail', 'share'];
    const showTab = (tab) => {
        tabs.forEach(t => {
            document.getElementById('tab-' + t).classList.toggle('hidden', t !== tab);
            document.getElementById('tab-' + t).classList.toggle('block', t === tab);
        });
    };
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            showTab(this.dataset.tab);
        });
    });
    showTab('main');
}); 