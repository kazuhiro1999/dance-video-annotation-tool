from flask import Flask, jsonify, render_template, request, send_from_directory
import os
import json 

app = Flask(__name__)

with open(os.path.join(app.root_path, "config.json"), 'r', encoding='utf-8') as f:
    config = json.load(f)

# ローカル動画ファイルを保存しているフォルダ
VIDEO_FOLDER = os.path.join(app.root_path, 'static', 'videos')
COMMENTS_FOLDER = os.path.join(app.root_path, 'static', 'comments')
EVALUATIONS_FOLDER = os.path.join(app.root_path, 'static', 'evaluations')


# メイン
@app.route('/')
def index():
    people = config.get('people', [])
    evaluation_items = config.get('evaluation_items', {})
    scores = config.get('scores', {})
    return render_template('index.html', people=people, evaluation_items=evaluation_items, scores=scores)


# 動画ファイルを提供するエンドポイント
@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_FOLDER, filename)


# コメントを提供するエンドポイント (GET, POST対応)
@app.route('/api/comments/<filename>', methods=['GET', 'POST'])
def serve_comments(filename):
    comment_file = os.path.join(COMMENTS_FOLDER, f"{filename}.json")
    
    if request.method == 'GET':
        # コメントファイルを読み込み、存在しない場合は空のリストを返す
        if os.path.exists(comment_file):
            with open(comment_file, 'r', encoding='utf-8') as f:
                comments = json.load(f)
        else:
            comments = []
        return jsonify(comments)
    
    elif request.method == 'POST':
        # POSTされたコメントを追加し、ファイルに保存
        new_comment = request.json
        if os.path.exists(comment_file):
            with open(comment_file, 'r', encoding='utf-8') as f:
                comments = json.load(f)
        else:
            comments = []
        comments.append(new_comment)
        with open(comment_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=4)
        return jsonify(comments), 201


# 評価を提供するエンドポイント (GET, POST対応)
@app.route('/api/evaluation/<filename>', methods=['GET', 'POST'])
def serve_evaluation(filename):
    evaluation_file = os.path.join(EVALUATIONS_FOLDER, f"{filename}.json")
    
    if request.method == 'GET':
        # 評価ファイルを読み込み、存在しない場合は空の辞書を返す
        if os.path.exists(evaluation_file):
            with open(evaluation_file, 'r', encoding='utf-8') as f:
                evaluation = json.load(f)
        else:
            evaluation = {}
        return jsonify(evaluation)
    
    elif request.method == 'POST':
        # POSTされた評価を保存
        new_evaluation = request.json
        with open(evaluation_file, 'w', encoding='utf-8') as f:
            json.dump(new_evaluation, f, ensure_ascii=False, indent=4)
        return jsonify(new_evaluation), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
