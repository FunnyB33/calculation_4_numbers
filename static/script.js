// static/script.js

document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('calc-form');
    var spinner = document.getElementById('spinner');
    var resultDiv = document.getElementById('result');
    var backButton = document.getElementById('back-button');

    form.addEventListener('submit', function(event) {
        // デフォルトのフォーム送信を停止
        event.preventDefault();

        // フォームと結果を非表示にし、スピナーを表示
        form.style.display = 'none';
        resultDiv.style.display = 'none';
        spinner.style.display = 'block';

        // 3秒後にフォームを送信
        setTimeout(function() {
            form.submit();
        }, 3000);
    });

    // ページ読み込み時にスピナーを非表示にし、結果を表示
    var resultExists = form.getAttribute('data-result-exists');
    if (resultExists === 'true') {
        form.style.display = 'none';
        resultDiv.style.display = 'block';
    } else {
        form.style.display = 'block';
        resultDiv.style.display = 'none';
    }

    // 「再度計算する」ボタンのクリックイベント
    if (backButton) {
        backButton.addEventListener('click', function() {
            resultDiv.style.display = 'none';
            form.style.display = 'block';
            // 入力フォームを空白にする
            form.reset();
        });
    }
});
