document.addEventListener('DOMContentLoaded', () => {
    const columnContainer = document.getElementById('column-view-container');
    const contentPanel = document.getElementById('content-panel');
    const welcomeMessage = document.getElementById('welcome-message');

    // ▼▼▼ 追加 ▼▼▼
    const mainContainer = document.querySelector('.main-container');
    const toggleSidebarBtn = document.getElementById('toggle-sidebar-btn');

    // サイドバー表示切替ボタンのイベントリスナー
    if (toggleSidebarBtn && mainContainer) {
        toggleSidebarBtn.addEventListener('click', () => {
            mainContainer.classList.toggle('sidebar-hidden');

            // アイコンも切り替えて分かりやすくする
            const icon = toggleSidebarBtn.querySelector('.material-symbols-outlined');
            if (icon) {
                icon.textContent = mainContainer.classList.contains('sidebar-hidden') ? 'menu_open' : 'menu';
            }
        });
    }
    // ▲▲▲ 追加 ▲▲▲

    let subjectsManifest = [];
    const loadedSubjectData = {};

    // 1. 初期化：目次を読み込み、最初のカラム（教科一覧）を表示
    async function initializeApp() {
        try {
            const response = await fetch('data/subjects.json');
            if (!response.ok) throw new Error('目次ファイルの読み込みに失敗');
            subjectsManifest = await response.json();
            renderSubjectsColumn(subjectsManifest);
        } catch (error) {
            console.error(error);
            contentPanel.innerHTML = `<p class="error-text">問題の読み込みに失敗しました。</p>`;
        }
    }

    // 2. カラムを生成する汎用関数
    function createColumn(title, items, level) {
        const column = document.createElement('div');
        column.className = 'column';
        column.dataset.level = level; // レベルをデータ属性として保持 (1:教科, 2:セット)

        let itemsHTML = items.map(item => `
            <li>
                <div class="list-item" data-id="${item.id}">
                    <i class="material-symbols-outlined">${item.icon || (level === 1 ? 'menu_book' : 'folder')}</i>
                    <span>${item.title}</span>
                </div>
            </li>
        `).join('');

        column.innerHTML = `
            <div class="column-title">${title}</div>
            <ul>${itemsHTML}</ul>
        `;

        // カラム内の項目がクリックされたときのイベントリスナー
        column.addEventListener('click', handleItemClick);
        return column;
    }

    // 3. 最初のカラム（教科一覧）を描画
    function renderSubjectsColumn(subjects) {
        const subjectsColumn = createColumn('教科', subjects, 1);
        columnContainer.appendChild(subjectsColumn);
    }

    // 4. カラム内の項目クリックを処理するメインロジック
    async function handleItemClick(event) {
        const item = event.target.closest('.list-item');
        if (!item) return;

        const column = item.closest('.column');
        const level = parseInt(column.dataset.level);
        const id = item.dataset.id;
        
        // --- UIの更新 ---
        // 同じカラム内の他のアクティブ項目を解除
        column.querySelectorAll('.list-item.active').forEach(activeItem => {
            activeItem.classList.remove('active');
        });
        item.classList.add('active'); // クリックされた項目をアクティブに

        // クリックされたカラムより後のカラムをすべて削除
        removeColumnsAfter(level);

        // --- 次のアクションを決定 ---
        if (level === 1) { // 教科がクリックされた場合
            const subjectData = await getSubjectData(id);
            if (subjectData && subjectData.contentSets) {
                const setsColumn = createColumn('問題セット', subjectData.contentSets, 2);
                columnContainer.appendChild(setsColumn);
                showWelcomeMessage('問題セットを選択してください。'); // メインパネルをリセット
            }
        } else if (level === 2) { // 問題セットがクリックされた場合
            const subjectId = column.previousElementSibling.querySelector('.list-item.active').dataset.id;
            const subjectData = loadedSubjectData[subjectId];
            const setData = subjectData.contentSets.find(s => s.id === id);
            if (setData) {
                renderQuestionPanel(setData); // メインパネルに問題を表示
            }
        }
    }

    // 5. 指定レベル以降のカラムを削除する関数
    function removeColumnsAfter(level) {
        Array.from(columnContainer.children).forEach(col => {
            if (parseInt(col.dataset.level) > level) {
                col.remove();
            }
        });
    }

    // 6. 問題詳細を右側のパネルに描画する関数
    function renderQuestionPanel(set) {
        welcomeMessage.classList.add('hidden');
        contentPanel.innerHTML = '';

        let contentHTML = `
            <h2 class="large-title primary-text">${set.title}</h2>
            <p class="medium-text" style="margin-bottom: 1.5rem;">${set.description}</p>
        `;

        set.questions.forEach(q => {
             contentHTML += `
                <article class="problem-card" id="problem-${q.id}">
                    <h4 class="medium-title primary-text">${q.q_num}</h4>
                    <div class="question-text">${q.question_text}</div>
                    <div class="problem-actions">
                        <button class="chip" data-action="toggle" data-target-id="hint-${q.id}">ヒント</button>
                        <button class="chip" data-action="toggle" data-target-id="answer-${q.id}">解答</button>
                        <button class="chip" data-action="toggle" data-target-id="explanation-${q.id}">解説</button>
                    </div>
                    <div id="hint-${q.id}" class="hint-content hidden"><p>${q.hint}</p></div>
                    <div id="answer-${q.id}" class="answer-content hidden"><p>${q.answer}</p></div>
                    <div id="explanation-${q.id}" class="explanation-content hidden"><p>${q.explanation}</p></div>
                </article>`;
        });
        
        contentPanel.innerHTML = contentHTML;

        if (set.isMath && window.MathJax) {
            MathJax.typesetPromise([contentPanel]).catch(err => console.error(err));
        }
    }
    
    // 7. ウェルカムメッセージを表示するヘルパー関数
    function showWelcomeMessage(text) {
        contentPanel.innerHTML = '';
        welcomeMessage.classList.remove('hidden');
        welcomeMessage.querySelector('p').textContent = text;
    }

    // 8. ヒント・解答の表示切り替え（変更なし）
    contentPanel.addEventListener('click', (e) => {
        const button = e.target.closest('button[data-action="toggle"]');
        if (!button) return;
        const targetElement = document.getElementById(button.dataset.targetId);
        if (targetElement) targetElement.classList.toggle('hidden');
    });

    // 9. データ取得（キャッシュ対応）（変更なし）
    async function getSubjectData(subjectId) {
        if (loadedSubjectData[subjectId]) return loadedSubjectData[subjectId];
        const subjectInfo = subjectsManifest.find(s => s.id === subjectId);
        if (!subjectInfo) return null;
        try {
            const response = await fetch(`data/${subjectInfo.file}`);
            if (!response.ok) throw new Error(`${subjectInfo.file}の読み込みに失敗`);
            const data = await response.json();
            loadedSubjectData[subjectId] = data;
            return data;
        } catch (error) { console.error(error); return null; }
    }
    
    initializeApp();
});