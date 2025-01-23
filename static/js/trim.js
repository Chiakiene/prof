document.addEventListener('DOMContentLoaded', function() {
    let cropper = null;
    let currentImageType = null; // 'avatar' または 'background'

    // アバターアップロードボタンのイベント
    document.getElementById('avatarUpload').addEventListener('click', function() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.onchange = e => handleImageSelect(e, 'avatar');
        input.click();
    });

    // 背景画像アップロードエリアのイベント
    const backgroundUpload = document.getElementById('backgroundUpload');
    backgroundUpload.addEventListener('click', function() {
        const input = backgroundUpload.querySelector('input[type="file"]');
        input.onchange = e => handleImageSelect(e, 'background');
        input.click();
    });

    // ドラッグ&ドロップ対応
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
            handleImageSelect({ target: { files: [file] } }, 'background');
        }
    });

    // 画像選択時の処理
    function handleImageSelect(event, type) {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = e => {
                currentImageType = type;
                showTrimModal(e.target.result, type);
            };
            reader.readAsDataURL(file);
        }
    }

    // トリミングモーダルの表示
    function showTrimModal(imageUrl, type) {
        const modal = document.getElementById('trimModal');
        const trimImage = document.getElementById('trimImage');
        
        modal.classList.add('active');
        trimImage.src = imageUrl;

        // 既存のCropperインスタンスを破棄
        if (cropper) {
            cropper.destroy();
        }

        // 新しいCropperインスタンスを作成
        const options = {
            aspectRatio: type === 'avatar' ? 1 : 16/9,
            viewMode: 2,
            preview: type === 'avatar' ? '#avatarPreview' : '#backgroundPreview',
            guides: true,
            autoCropArea: 1,
        };

        cropper = new Cropper(trimImage, options);
    }

    // コントロールボタンのイベント
    document.getElementById('zoomIn').addEventListener('click', () => cropper.zoom(0.1));
    document.getElementById('zoomOut').addEventListener('click', () => cropper.zoom(-0.1));
    document.getElementById('rotateLeft').addEventListener('click', () => cropper.rotate(-90));
    document.getElementById('rotateRight').addEventListener('click', () => cropper.rotate(90));
    document.getElementById('resetTransform').addEventListener('click', () => cropper.reset());

    // ズームスライダーのイベント
    document.getElementById('zoomSlider').addEventListener('input', function() {
        const value = (this.value - 50) / 100;
        cropper.zoomTo(1 + value);
    });

    // モーダルを閉じる
    document.getElementById('closeTrimModal').addEventListener('click', closeTrimModal);
    document.getElementById('cancelTrim').addEventListener('click', closeTrimModal);

    function closeTrimModal() {
        const modal = document.getElementById('trimModal');
        modal.classList.remove('active');
        if (cropper) {
            cropper.destroy();
            cropper = null;
        }
    }

    // トリミング画像の保存
    document.getElementById('saveTrim').addEventListener('click', function() {
        if (!cropper) return;

        const canvas = cropper.getCroppedCanvas({
            width: currentImageType === 'avatar' ? 400 : 1200,
            height: currentImageType === 'avatar' ? 400 : 675,
        });

        canvas.toBlob(blob => {
            const formData = new FormData();
            formData.append('image', blob);
            formData.append('type', currentImageType);

            // サーバーに画像をアップロード
            fetch('/upload_image', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 画像の更新
                    if (currentImageType === 'avatar') {
                        document.querySelector('.profile-image img').src = data.url;
                    }
                    closeTrimModal();
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
}); 