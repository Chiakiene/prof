let cropper = null;
let currentImageType = null;

// トリミングモーダルを表示
function showCropModal(image, type) {
    const modal = document.getElementById('cropModal');
    const cropImage = document.getElementById('cropImage');
    
    currentImageType = type;
    cropImage.src = image.src;
    modal.style.display = 'block';
    
    // 既存のCropperインスタンスを破棄
    if (cropper) {
        cropper.destroy();
    }
    
    // 新しいCropperインスタンスを作成
    cropper = new Cropper(cropImage, {
        aspectRatio: type === 'avatar' ? 1 : 16/9,
        viewMode: 1,
        dragMode: 'move',
        autoCropArea: 1,
        restore: false,
        guides: true,
        center: true,
        highlight: false,
        cropBoxMovable: true,
        cropBoxResizable: true,
        toggleDragModeOnDblclick: false,
    });
}

// モーダルを閉じる
function closeCropModal() {
    const modal = document.getElementById('cropModal');
    modal.style.display = 'none';
    
    if (cropper) {
        cropper.destroy();
        cropper = null;
    }
}

// ズーム調整
function adjustZoom(delta) {
    if (cropper) {
        const currentZoom = cropper.getCanvasData().width / cropper.getContainerData().width;
        cropper.zoomTo(currentZoom + delta);
    }
}

// 回転
function rotateImage(degree) {
    if (cropper) {
        cropper.rotate(degree);
    }
}

// 反転
function flipImage(direction) {
    if (cropper) {
        if (direction === 'horizontal') {
            cropper.scaleX(-cropper.getData().scaleX || -1);
        } else {
            cropper.scaleY(-cropper.getData().scaleY || -1);
        }
    }
}

// トリミング画像の保存
function saveCroppedImage() {
    if (!cropper) return;
    
    // キャンバスからBlobを取得
    cropper.getCroppedCanvas().toBlob(function(blob) {
        // FormDataの作成
        const formData = new FormData();
        formData.append('image', blob, 'cropped.jpg');
        formData.append('type', currentImageType);
        
        // サーバーにアップロード
        fetch('/upload_image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (currentImageType === 'avatar') {
                    // アバター画像の更新
                    document.querySelector('.profile-image img').src = data.url;
                } else {
                    // 背景画像の更新
                    const backgroundPreview = document.querySelector('.background-preview');
                    if (backgroundPreview) {
                        backgroundPreview.querySelector('img').src = data.url;
                    } else {
                        const uploadArea = document.getElementById('backgroundUpload');
                        uploadArea.innerHTML = `
                            <div class="background-preview">
                                <img src="${data.url}" alt="背景画像">
                                <button type="button" class="delete-image" onclick="deleteBackgroundImage()">
                                    <i data-feather="trash-2"></i>
                                </button>
                            </div>
                        `;
                        feather.replace();
                    }
                    updateDesignPreview();
                }
                closeCropModal();
            }
        })
        .catch(error => console.error('Error:', error));
    }, 'image/jpeg');
}

// ズームスライダーの制御
document.addEventListener('DOMContentLoaded', function() {
    const zoomRange = document.getElementById('zoomRange');
    if (zoomRange) {
        zoomRange.addEventListener('input', function() {
            if (cropper) {
                cropper.zoomTo(this.value);
            }
        });
    }
}); 