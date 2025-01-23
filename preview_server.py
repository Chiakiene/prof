from flask import Flask, render_template, url_for

app = Flask(__name__)

# テスト用のユーザーデータ
class MockUser:
    def __init__(self):
        self.user_id = "test123"
        self.username = "テストユーザー"
        self.email = "test@example.com"
        self.bio = "これはテストユーザーの自己紹介です。"
        self.location = "東京"
        self.website = "https://example.com"
        self.avatar_url = None
        self.custom_fields = []
        self.design = MockDesign()
        self.sponsors = []
        self.sponsorship_tiers = []

class MockDesign:
    def __init__(self):
        self.background_type = "color"
        self.background_color = "#f7f9fc"
        self.background_image = None
        self.background_opacity = 1.0
        self.text_color = "#2c3e50"
        self.accent_color = "#4a90e2"
        self.font_family = "'Noto Sans JP', sans-serif"
        self.font_size = 16
        self.heading_size = 24

# 現在のユーザーをモック
current_user = MockUser()

@app.route('/')
def preview_profile():
    return render_template('profile.html', current_user=current_user)

@app.route('/<user_id>')
def user_profile(user_id):
    # プレビュー用なので同じページを返す
    return render_template('profile.html', current_user=current_user)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

# URLを生成するためのコンテキストプロセッサを追加
@app.context_processor
def utility_processor():
    def mock_url_for(endpoint, **kwargs):
        if endpoint == 'user_profile':
            return f"/{kwargs.get('user_id', '')}"
        elif endpoint == 'static':
            return f"/static/{kwargs.get('filename', '')}"
        elif endpoint == 'index':
            return "/"
        elif endpoint == 'logout':
            return "/logout"
        elif endpoint == 'profile':
            return "/"
        return "#"
    return dict(url_for=mock_url_for)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 