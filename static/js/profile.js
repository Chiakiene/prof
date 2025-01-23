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

// メインのDOMContentLoadedイベントリスナー
document.addEventListener('DOMContentLoaded', function() {
    // アバターアップロード機能
    initializeAvatarUpload();
    
    // パスワード表示切り替え
    initializePasswordToggle();
    
    // 文字数カウント
    initializeCharCount();
    
    // 折りたたみセクション
    initializeCollapsible();
    
    // フォームバリデーション
    initializeFormValidation();
    
    // カスタムフィールド
    initializeCustomFields();
});

// アバターアップロード機能の初期化
function initializeAvatarUpload() {
    const avatarInput = document.getElementById('avatarInput');
    const uploadButton = document.getElementById('uploadAvatar');
    const cropModal = document.getElementById('cropModal');
    const cropImage = document.getElementById('cropImage');
    const avatarPreview = document.getElementById('avatarPreview');
    
    let cropper = null;

    // アップロードボタンのクリックイベント
    uploadButton?.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log('Upload button clicked'); // デバッグ用
        avatarInput?.click();
    });

    // ファイル選択時のイベント
    avatarInput?.addEventListener('change', function(e) {
        console.log('File selected'); // デバッグ用
        const file = e.target.files?.[0];
        if (!file) return;

        // ファイルサイズチェック
        if (file.size > 5 * 1024 * 1024) {
            showMessage('ファイルサイズは5MB以下にしてください', 'error');
            return;
        }

        // ファイル形式チェック
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
        if (!allowedTypes.includes(file.type)) {
            showMessage('JPG、PNG、GIF形式の画像のみアップロード可能です', 'error');
            return;
        }

        // 画像プレビュー
        const reader = new FileReader();
        reader.onload = function(e) {
            console.log('File loaded'); // デバッグ用
            if (cropImage && cropModal && e.target?.result) {
                cropImage.src = e.target.result;
                cropModal.style.display = 'block';

                if (cropper) {
                    cropper.destroy();
                }
                cropper = new Cropper(cropImage, {
                    aspectRatio: 1,
                    viewMode: 1,
                    autoCropArea: 1,
                    background: false
                });
            }
        };
        reader.readAsDataURL(file);
    });

    // モーダルを閉じる
    document.querySelectorAll('.modal-close, #cancelCrop').forEach(button => {
        button?.addEventListener('click', () => {
            closeModal();
        });
    });

    // クロップ画像を保存
    document.getElementById('saveCrop')?.addEventListener('click', async function() {
        if (!cropper) return;
        
        try {
            const canvas = cropper.getCroppedCanvas({
                width: 800,
                height: 800
            });
            
            const blob = await new Promise(resolve => {
                canvas.toBlob(resolve, 'image/jpeg', 0.85);
            });
            
            const formData = new FormData();
            formData.append('avatar', blob, 'avatar.jpg');
            
            const response = await fetch('/profile/avatar/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            if (data.success) {
                updateAvatarImages(data.avatar_url);
                showMessage(data.message, 'success');
            } else {
                showMessage(data.message, 'error');
            }
            
            closeModal();
            
        } catch (error) {
            console.error('アップロードエラー:', error);
            showMessage('エラーが発生しました', 'error');
        }
    });

    // モーダルを閉じる関数
    function closeModal() {
        if (cropModal) {
            cropModal.style.display = 'none';
        }
        if (cropper) {
            cropper.destroy();
            cropper = null;
        }
        if (avatarInput) {
            avatarInput.value = '';
        }
    }

    // アバター画像を更新する関数
    function updateAvatarImages(newUrl) {
        // プレビュー画像の更新
        if (avatarPreview) {
            if (avatarPreview.tagName.toLowerCase() === 'img') {
                avatarPreview.src = newUrl;
            } else {
                const img = document.createElement('img');
                img.src = newUrl;
                img.alt = 'プロフィール画像';
                img.id = 'avatarPreview';
                img.className = 'avatar-large';
                avatarPreview.parentNode.replaceChild(img, avatarPreview);
            }
        }

        // ナビバーのアバター更新
        const navAvatar = document.querySelector('.nav-avatar');
        if (navAvatar) {
            if (navAvatar.tagName.toLowerCase() === 'img') {
                navAvatar.src = newUrl;
            } else {
                const img = document.createElement('img');
                img.src = newUrl;
                img.alt = 'プロフィール画像';
                img.className = 'nav-avatar';
                navAvatar.parentNode.replaceChild(img, navAvatar);
            }
        }
    }
}

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

// パスワード表示切り替え
function initializePasswordToggle() {
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
}

// 文字数カウント
function initializeCharCount() {
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
}

// 折りたたみセクション
function initializeCollapsible() {
    document.querySelectorAll('.collapsible-header').forEach(header => {
        header.addEventListener('click', function() {
            this.parentElement.classList.toggle('active');
        });
    });
}

// フォームバリデーション
function initializeFormValidation() {
    const form = document.querySelector('.profile-form');
    if (form) {
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
    }
}

// カスタムフィールドの管理
function initializeCustomFields() {
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
} 