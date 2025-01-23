// デザインプレビューの更新
function updateDesignPreview() {
    const preview = document.getElementById('designPreview');
    if (!preview) return;

    // 背景設定の取得
    const backgroundType = document.querySelector('input[name="background_type"]:checked').value;
    const backgroundColor = document.getElementById('background_color').value;
    const backgroundOpacity = document.getElementById('background_opacity').value / 100;
    
    // フォント設定の取得
    const fontFamily = document.getElementById('font_family').value;
    const fontSize = document.getElementById('font_size').value;
    const textColor = document.getElementById('text_color').value;

    // プレビューの更新
    preview.style.fontFamily = fontFamily;
    preview.style.color = textColor;
    
    // 背景の設定
    if (backgroundType === 'color') {
        preview.style.backgroundColor = backgroundColor;
        preview.style.backgroundImage = 'none';
    } else {
        const backgroundImage = document.querySelector('.background-preview img');
        if (backgroundImage) {
            preview.style.backgroundImage = `url(${backgroundImage.src})`;
            preview.style.backgroundSize = 'cover';
            preview.style.backgroundPosition = 'center';
        }
    }
    
    // 背景の透過度
    preview.style.setProperty('--preview-opacity', backgroundOpacity);

    // フォントサイズの設定
    const previewContent = preview.querySelector('.preview-content');
    if (previewContent) {
        previewContent.style.fontSize = `${fontSize}px`;
    }
}

// イベントリスナーの設定
document.addEventListener('DOMContentLoaded', function() {
    // 背景タイプの切り替え
    const backgroundTypeInputs = document.querySelectorAll('input[name="background_type"]');
    backgroundTypeInputs.forEach(input => {
        input.addEventListener('change', function() {
            const colorGroup = document.getElementById('backgroundColorGroup');
            const imageGroup = document.getElementById('backgroundImageGroup');
            
            if (this.value === 'color') {
                colorGroup.style.display = 'block';
                imageGroup.style.display = 'none';
            } else {
                colorGroup.style.display = 'none';
                imageGroup.style.display = 'block';
            }
            
            updateDesignPreview();
        });
    });

    // カラーピッカーの更新
    const colorInputs = document.querySelectorAll('input[type="color"]');
    colorInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.nextElementSibling.textContent = this.value;
            updateDesignPreview();
        });
    });

    // レンジスライダーの更新
    const rangeInputs = document.querySelectorAll('input[type="range"]');
    rangeInputs.forEach(input => {
        input.addEventListener('input', function() {
            this.nextElementSibling.textContent = 
                this.id === 'background_opacity' ? `${this.value}%` : `${this.value}px`;
            updateDesignPreview();
        });
    });

    // フォント選択の更新
    const fontSelect = document.getElementById('font_family');
    if (fontSelect) {
        fontSelect.addEventListener('change', updateDesignPreview);
    }

    // 背景画像のドラッグ&ドロップ
    const backgroundUpload = document.getElementById('backgroundUpload');
    if (backgroundUpload) {
        backgroundUpload.addEventListener('dragover', e => {
            e.preventDefault();
            backgroundUpload.classList.add('drag-over');
        });

        backgroundUpload.addEventListener('dragleave', () => {
            backgroundUpload.classList.remove('drag-over');
        });

        backgroundUpload.addEventListener('drop', e => {
            e.preventDefault();
            backgroundUpload.classList.remove('drag-over');
            const file = e.dataTransfer.files[0];
            if (file && file.type.startsWith('image/')) {
                handleImageUpload({ files: [file] }, 'background');
            }
        });
    }

    // 初期プレビューの更新
    updateDesignPreview();
});

// 背景画像の削除
function deleteBackgroundImage() {
    if (confirm('背景画像を削除してもよろしいですか？')) {
        fetch('/delete_background_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const preview = document.querySelector('.background-preview');
                if (preview) {
                    preview.remove();
                }
                document.getElementById('bg_type_color').checked = true;
                const event = new Event('change');
                document.getElementById('bg_type_color').dispatchEvent(event);
            }
        })
        .catch(error => console.error('Error:', error));
    }
} 