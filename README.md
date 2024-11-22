# Dance Video Annotation Tool

ダンスのパフォーマンス評価・アノテーションを行うためのWebベースツールです。動画を閲覧しながら、複数の評価項目についてスコアリングとコメントを付けることができます。  
<br>
![dance-video-annotation-tool メインページ](https://github.com/user-attachments/assets/2924cb8e-62c4-4cb7-82c3-4e498cc6f3e7)  

## 機能

- 動画の再生・閲覧
- 7つの評価項目（力強さ、緩急、動きの大きさ、リズム、正確さ、バランス、表情）での10段階評価
- タイムスタンプ付きコメント機能
- 評価結果のJSON形式での保存

## システム要件

- Python 3.8以上
- Flask

## インストール方法

1. リポジトリをクローン
```bash
git clone https://github.com/kazuhiro1999/dance-video-annotation-tool.git
cd dance-video-annotation-tool
```

2. 必要なパッケージをインストール
```bash
pip install flask
```

## プロジェクト構成

```
dance-video-annotation/
├── app.py                 # メインのFlaskアプリケーション
├── config.json            # 設定ファイル（評価項目、スコア基準など）
├── static/
│   ├── videos/           # 評価対象の動画ファイル
│   ├── comments/         # コメントデータ（JSON）
│   └── evaluations/      # 評価データ（JSON）
├── templates/
│   └── index.html        # メインページのテンプレート
└── README.md             # 本ファイル

```

## データの配置方法

### 1. 動画ファイル

- `static/videos/` ディレクトリに評価対象の動画ファイルを配置
- ファイル名の形式: `[dancer_id].mp4`

### 2. 設定ファイル (config.json)

以下の3つの主要セクションで構成:

1. `people`: 評価対象者の情報
```json
{
    "id": "dancer_001",
    "name": "ダンサー1"
}
```

2. `evaluation_items`: 評価項目の定義  
- 各項目に対して名前、説明、詳細な評価基準を設定

3. `scores`: 10段階評価の各スコアの定義  
- 各スコアのレベルと詳細な説明を設定

### 3. コメント・評価データ

- コメント: `static/comments/[dancer_id].json`
- 評価データ: `static/evaluations/[dancer_id].json`
- 自動的に作成・更新されます

## 使用方法

1. サーバーの起動
```bash
python app.py
```

2. ブラウザでアクセス
```
http://localhost:5555
```

## API エンドポイント

### 動画の提供
- GET `/videos/<filename>`

### コメントの取得・保存
- GET `/api/comments/<filename>`
- POST `/api/comments/<filename>`

### 評価の取得・保存
- GET `/api/evaluation/<filename>`
- POST `/api/evaluation/<filename>`

## 開発者向け情報

### デバッグモード

開発時は `app.py` の最後で設定されているデバッグモードを活用できます:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
```

### 新しい評価項目の追加

1. `config.json` の `evaluation_items` セクションに新しい項目を追加
2. 必要に応じて `templates/index.html` の表示部分を更新

