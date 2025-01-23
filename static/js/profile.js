// デザインプレビューの更新
function updateDesignPreview() {
    const preview = document.getElementById('designPreview');
    const backgroundType = document.querySelector('input[name="background_type"]:checked').value;
    const backgroundColor = document.getElementById('background_color').value;
    const textColor = document.getElementById('text_color').value;
    const textBorderEnabled = document.querySelector('input[name="text_border_enabled"]:checked').value === 'true';
    const textBorderColor = document.getElementById('text_border_color').value;
    const textBorderSize = document.getElementById('text_border_size').value;
    const opacity = document.getElementById('background_opacity').value / 100;
    const fontFamily = document.getElementById('font_family').value;
    const fontSize = document.getElementById('font_size').value;
    const headingSize = document.getElementById('heading_size').value;

    // プレビューコンテンツの設定
    preview.innerHTML = `
        <div class="preview-background"></div>
        <div class="preview-content">
            <h3>プレビュー</h3>
            <p>ここにプレビューが表示されます</p>
            <a href="#">リンクのサンプル</a>
        </div>
    `;

    // 背景の設定
    const previewBg = preview.querySelector('.preview-background');
    if (backgroundType === 'color') {
        previewBg.style.backgroundColor = backgroundColor;
        previewBg.style.backgroundImage = 'none';
    } else if (backgroundType === 'image') {
        const backgroundImage = document.querySelector('.background-image-preview img');
        if (backgroundImage) {
            previewBg.style.backgroundImage = `url(${backgroundImage.src})`;
            previewBg.style.backgroundColor = 'transparent';
        }
    }
    previewBg.style.opacity = opacity;

    // プレビューコンテンツのスタイル設定
    const previewContent = preview.querySelector('.preview-content');
    previewContent.style.color = textColor;
    previewContent.style.fontFamily = fontFamily;
    previewContent.style.fontSize = `${fontSize}px`;

    // 見出しのスタイル
    const heading = preview.querySelector('h3');
    heading.style.fontSize = `${headingSize}px`;

    // 文字枠の設定
    if (textBorderEnabled) {
        const textShadow = `
            -${textBorderSize}px -${textBorderSize}px 2px ${textBorderColor},
            ${textBorderSize}px -${textBorderSize}px 2px ${textBorderColor},
            -${textBorderSize}px ${textBorderSize}px 2px ${textBorderColor},
            ${textBorderSize}px ${textBorderSize}px 2px ${textBorderColor},
            0 0 4px ${textBorderColor}
        `;
        previewContent.style.textShadow = textShadow;
    } else {
        previewContent.style.textShadow = 'none';
    }
}

// タブの切り替え
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // アクティブなタブを切り替え
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            this.classList.add('active');
            document.getElementById(`${this.dataset.tab}-tab`).classList.add('active');
        });
    });
    
    // プロフィールURLのコピー機能
    const copyButton = document.querySelector('.copy-button');
    if (copyButton) {
        copyButton.addEventListener('click', copyProfileUrl);
    }
    
    // カスタムフィールドの初期カウント更新
    updateFieldCount();
});

// プロフィールURLをクリップボードにコピー
function copyProfileUrl() {
    const urlInput = document.querySelector('.profile-url input');
    urlInput.select();
    document.execCommand('copy');
    
    // コピー完了のフィードバック
    const copyButton = document.querySelector('.copy-button');
    const originalIcon = copyButton.innerHTML;
    copyButton.innerHTML = '<i data-feather="check"></i>';
    feather.replace();
    
    setTimeout(() => {
        copyButton.innerHTML = originalIcon;
        feather.replace();
    }, 2000);
}

// カスタムフィールドの追加
function addCustomField() {
    const container = document.getElementById('custom-fields-container');
    const currentCount = container.children.length;
    const maxFields = parseInt(document.querySelector('.field-counter').textContent.split('/')[1]);
    
    if (currentCount >= maxFields) {
        alert('これ以上項目を追加できません');
        return;
    }
    
    const fieldHtml = `
        <div class="custom-field">
            <div class="field-header">
                <input type="text" name="custom_labels[]" placeholder="項目名" maxlength="50">
                <button type="button" class="remove-field" onclick="removeCustomField(this)">
                    <i data-feather="x"></i>
                </button>
            </div>
            <input type="text" name="custom_values[]" placeholder="内容" maxlength="200">
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', fieldHtml);
    feather.replace();
    updateFieldCount();
}

// カスタムフィールドの削除
function removeCustomField(button) {
    button.closest('.custom-field').remove();
    updateFieldCount();
}

// カスタムフィールドの数を更新
function updateFieldCount() {
    const container = document.getElementById('custom-fields-container');
    const countElement = document.getElementById('field-count');
    if (container && countElement) {
        countElement.textContent = container.children.length;
    }
}

// 画像アップロード処理
function handleImageUpload(input, type) {
    const file = input.files[0];
    if (!file) return;
    
    // 画像ファイルかチェック
    if (!file.type.startsWith('image/')) {
        alert('画像ファイルを選択してください');
        return;
    }
    
    // ファイルサイズチェック（5MB以下）
    if (file.size > 5 * 1024 * 1024) {
        alert('ファイルサイズは5MB以下にしてください');
        return;
    }
    
    // 画像をプレビュー表示してからトリミングモーダルを表示
    const reader = new FileReader();
    reader.onload = function(e) {
        const image = new Image();
        image.src = e.target.result;
        image.onload = function() {
            showCropModal(image, type);
        };
    };
    reader.readAsDataURL(file);
}

// カラーピッカーの値表示更新
function updateColorValue(input) {
    const wrapper = input.closest('.color-picker-wrapper');
    const valueDisplay = wrapper.querySelector('.color-value');
    valueDisplay.textContent = input.value;
    updateDesignPreview();
}

// 背景画像削除機能
async function deleteBackgroundImage() {
    if (confirm('背景画像を削除してもよろしいですか？')) {
        try {
            const response = await fetch('/api/delete-background', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            if (response.ok) {
                // プレビューを更新
                const preview = document.querySelector('.background-image-preview');
                if (preview) {
                    preview.remove();
                }
                // 背景タイプを色に切り替え
                document.getElementById('bg_type_color').checked = true;
                const colorOptions = document.querySelector('.color-options');
                const imageOptions = document.querySelector('.image-options');
                colorOptions.style.display = 'block';
                imageOptions.style.display = 'none';

                // プレビューの背景をリセット
                const designPreview = document.getElementById('designPreview');
                designPreview.style.setProperty('--preview-background-image', 'none');
                updateDesignPreview();
            } else {
                alert('画像の削除に失敗しました');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('エラーが発生しました');
        }
    }
}

// 初期化
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    updateFieldCount();
    updateDesignPreview();
    feather.replace();

    // カラーピッカーのイベントリスナー
    document.querySelectorAll('input[type="color"]').forEach(input => {
        input.addEventListener('input', () => {
            updateColorValue(input);
            updateDesignPreview();  // 直接プレビューを更新
        });
    });

    // 背景タイプのイベントリスナー
    document.querySelectorAll('input[name="background_type"]').forEach(radio => {
        radio.addEventListener('change', function() {
            const colorOptions = document.querySelector('.color-options');
            const imageOptions = document.querySelector('.image-options');
            
            if (this.value === 'color') {
                colorOptions.style.display = 'block';
                imageOptions.style.display = 'none';
            } else {
                colorOptions.style.display = 'none';
                imageOptions.style.display = 'block';
            }
            
            updateDesignPreview();
        });
    });

    // 各種入力要素のイベントリスナー
    const inputs = [
        { id: 'background_opacity', event: 'input', suffix: '%' },
        { id: 'font_size', event: 'input', suffix: 'px' },
        { id: 'heading_size', event: 'input', suffix: 'px' },
        { id: 'text_border_size', event: 'input', suffix: 'px' },
        { id: 'text_border_color', event: 'input' },  // 文字枠の色を追加
        { id: 'font_family', event: 'change' },
        { id: 'background_image', event: 'change' }
    ];

    inputs.forEach(({ id, event, suffix }) => {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener(event, () => {
                if (suffix) {
                    const valueDisplay = document.getElementById(`${id}-value`);
                    if (valueDisplay) {
                        valueDisplay.textContent = element.value + suffix;
                    }
                }
                // カラーピッカーの場合は値の表示も更新
                if (element.type === 'color') {
                    updateColorValue(element);
                }
                updateDesignPreview();
            });
        }
    });

    // 文字枠の有効/無効のイベントリスナー
    document.querySelectorAll('input[name="text_border_enabled"]').forEach(radio => {
        radio.addEventListener('change', function() {
            const borderOptions = document.querySelector('.text-border-options');
            const preview = document.getElementById('designPreview');
            const previewHeading = preview.querySelector('h3');

            if (this.value === 'true') {
                borderOptions.style.display = 'block';
                // 即座にプレビューを更新
                updateDesignPreview();
            } else {
                borderOptions.style.display = 'none';
                // 縁取りをすぐに解除
                preview.style.textShadow = 'none';
                if (previewHeading) {
                    previewHeading.style.textShadow = 'none';
                }
                // プレビューを更新
                updateDesignPreview();
            }
        });
    });

    // すべてのラジオボタンに即時更新を適用
    document.querySelectorAll('input[type="radio"]').forEach(radio => {
        radio.addEventListener('change', () => {
            updateDesignPreview();
        });
    });

    // アバターアップロード
    const avatarUpload = document.getElementById('avatarUpload');
    if (avatarUpload) {
        avatarUpload.addEventListener('click', function() {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = 'image/*';
            input.onchange = function(e) {
                handleImageUpload(this, 'avatar');
            };
            input.click();
        });
    }

    // フォームのバリデーション
    const form = document.querySelector('.settings-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const username = document.getElementById('username');
            if (username.value.length < 3) {
                e.preventDefault();
                alert('ユーザー名は3文字以上で入力してください');
                username.focus();
                return;
            }
            
            // カスタムフィールドのバリデーション
            const labels = document.getElementsByName('custom_labels[]');
            const values = document.getElementsByName('custom_values[]');
            for (let i = 0; i < labels.length; i++) {
                if (labels[i].value && !values[i].value) {
                    e.preventDefault();
                    alert('項目名を入力した場合は、内容も入力してください');
                    values[i].focus();
                    return;
                }
            }
        });
    }

    // 初期カウント更新
    updateFieldCount();
});

let cropper = null;
let currentImageType = null;

document.addEventListener('DOMContentLoaded', function() {
    // 要素の取得
    const modal = document.getElementById('uploadModal');
    const avatarUpload = document.getElementById('avatarUpload');
    const imageInput = document.getElementById('imageInput');
    const selectImage = document.getElementById('selectImage');
    const preview = document.getElementById('preview');
    const previewContainer = document.getElementById('previewContainer');
    const uploadButton = document.getElementById('uploadImage');
    
    // フォームのバリデーション
    const form = document.querySelector('.profile-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const username = document.getElementById('username');
            if (username && username.value.length < 3) {
                e.preventDefault();
                showMessage('ユーザー名は3文字以上で入力してください', 'error');
                username.focus();
            }
        });
    }
    
    // 画像アップロード関連の処理
    function initializeImageUpload() {
        avatarUpload.addEventListener('click', () => modal.style.display = 'block');
        document.querySelectorAll('.modal-close, #cancelUpload').forEach(button => {
            button.addEventListener('click', closeModal);
        });
        selectImage.addEventListener('click', () => imageInput.click());
        imageInput.addEventListener('change', handleImagePreview);
        uploadButton.addEventListener('click', handleImageUpload);
    }
    
    // プレビュー表示の処理
    function handleImagePreview(e) {
        const file = e.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                previewContainer.style.display = 'block';
                uploadButton.disabled = false;
            };
            reader.readAsDataURL(file);
        }
    }
    
    // 画像アップロードの処理
    async function handleImageUpload() {
        const file = imageInput.files[0];
        if (!file) return;
        
        const formData = new FormData();
        formData.append('image', file);
        
        try {
            const response = await fetch('/profile/upload_image', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                updateAvatar(data.url);
                closeModal();
                showMessage('プロフィール画像を更新しました', 'success');
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            showMessage('画像のアップロードに失敗しました', 'error');
        }
    }
    
    // アバター画像の更新
    function updateAvatar(url) {
        const avatar = document.querySelector('.avatar');
        if (avatar) {
            avatar.src = url;
        }
    }
    
    // モーダルを閉じる
    function closeModal() {
        modal.style.display = 'none';
        previewContainer.style.display = 'none';
        imageInput.value = '';
        uploadButton.disabled = true;
    }
    
    // メッセージの表示
    function showMessage(message, type = 'success') {
        const flashContainer = document.createElement('div');
        flashContainer.className = `flash flash-${type}`;
        flashContainer.textContent = message;
        
        document.querySelector('.profile-container').insertAdjacentElement('afterbegin', flashContainer);
        
        setTimeout(() => {
            flashContainer.remove();
        }, 3000);
    }
    
    // 初期化
    initializeImageUpload();
});

// カスタムフィールドの管理
document.addEventListener('DOMContentLoaded', function() {
    const customFields = document.getElementById('customFields');
    const addButton = document.getElementById('addField');
    
    // Sortable初期化
    if (customFields) {
        new Sortable(customFields, {
            animation: 150,
            handle: '.drag-handle',
            ghostClass: 'dragging',
            dragClass: 'dragging',
            onEnd: function() {
                updateFieldOrder();
            }
        });
    }
    
    function createField(index) {
        const field = document.createElement('div');
        field.className = 'custom-field';
        field.innerHTML = `
            <div class="drag-handle">
                <i data-feather="grip-vertical"></i>
            </div>
            <div class="field-inputs">
                <div class="form-group">
                    <input type="text" name="label_${index}" 
                           placeholder="ラベル" maxlength="50">
                </div>
                <div class="form-group">
                    <input type="text" name="value_${index}" 
                           placeholder="値" maxlength="500">
                </div>
            </div>
            <button type="button" class="button-icon remove-field" title="削除">
                <i data-feather="trash-2"></i>
            </button>
        `;
        return field;
    }
    
    if (addButton) {
        addButton.addEventListener('click', function() {
            const fields = customFields.children;
            if (fields.length >= 20) {
                showMessage('カスタムフィールドは20個までです', 'error');
                return;
            }
            
            const newField = createField(fields.length);
            customFields.appendChild(newField);
            feather.replace();
            
            if (fields.length >= 19) {
                addButton.disabled = true;
            }
        });
    }
    
    if (customFields) {
        customFields.addEventListener('click', function(e) {
            if (e.target.closest('.remove-field')) {
                e.target.closest('.custom-field').remove();
                if (addButton) {
                    addButton.disabled = false;
                }
                updateFieldOrder();
            }
        });
    }
});

// カスタムフィールドの順序を更新
function updateFieldOrder() {
    const fields = document.querySelectorAll('.custom-field');
    fields.forEach((field, index) => {
        const labelInput = field.querySelector('input[name^="label_"]');
        const valueInput = field.querySelector('input[name^="value_"]');
        
        if (labelInput) {
            labelInput.name = `label_${index}`;
        }
        if (valueInput) {
            valueInput.name = `value_${index}`;
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // パスワード表示切り替え
    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.setAttribute('data-feather', 'eye-off');
            } else {
                input.type = 'password';
                icon.setAttribute('data-feather', 'eye');
            }
            feather.replace();
        });
    });

    // 文字数カウント
    const bioTextarea = document.getElementById('bio');
    const charCount = document.querySelector('.char-count');
    
    function updateCharCount() {
        const count = bioTextarea.value.length;
        charCount.textContent = `${count}/1000`;
        if (count > 900) {
            charCount.style.color = count >= 1000 ? 'var(--error)' : 'var(--warning)';
        } else {
            charCount.style.color = 'var(--text-light)';
        }
    }
    
    bioTextarea.addEventListener('input', updateCharCount);
    updateCharCount();

    // 折りたたみセクション
    document.querySelectorAll('.collapsible-header').forEach(header => {
        header.addEventListener('click', function() {
            this.parentElement.classList.toggle('active');
        });
    });

    // フォームのバリデーション
    const form = document.querySelector('.profile-form');
    form.addEventListener('submit', function(e) {
        const newPassword = document.getElementById('new_password');
        const confirmPassword = document.getElementById('confirm_password');
        
        if (newPassword.value || confirmPassword.value) {
            if (newPassword.value !== confirmPassword.value) {
                e.preventDefault();
                showMessage('新しいパスワードが一致しません', 'error');
                return;
            }
            
            if (!document.getElementById('current_password').value) {
                e.preventDefault();
                showMessage('現在のパスワードを入力してください', 'error');
                return;
            }
        }
    });
}); 