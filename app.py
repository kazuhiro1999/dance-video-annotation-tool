import os
import json 
from flask import Flask, abort, jsonify, render_template, request, send_from_directory
from translations import all_translations, localize_config

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
    lang = request.args.get('lang', 'ja')
    trans = all_translations.get(lang, all_translations['ja'])
    localized_config = localize_config(config, lang)
    
    people = localized_config.get('people', [])
    evaluation_items = localized_config.get('evaluation_items', {})
    scores = localized_config.get('scores', {})
    return render_template('index.html', 
                           people=people, 
                           evaluation_items=evaluation_items, 
                           scores=scores,
                           _=lambda x: trans.get(x, x))


# 動画ファイルを提供するエンドポイント
@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_FOLDER, filename)


# コメントを提供するエンドポイント (GET, POST対応)
@app.route('/api/comments/<filename>', methods=['GET', 'POST', 'PUT', 'DELETE'])
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
    
@app.route('/api/comments/<person_id>/<comment_id>', methods=['PUT', 'DELETE'])
def update_or_delete_comment(person_id, comment_id):
    comment_file = os.path.join(COMMENTS_FOLDER, f"{person_id}.json")
    index = int(comment_id)

    if not os.path.exists(comment_file):
        return jsonify({"error": "コメントが見つかりません"}), 404

    with open(comment_file, 'r', encoding='utf-8') as f:
        comments = json.load(f)

    if request.method == 'PUT':
        # コメントを更新
        updated_comment = request.json
        if index < len(comments):
            comment = comments[index]
            comment.update(text=updated_comment)
        else:
            return jsonify({"error": "該当するコメントが見つかりません"}), 404

        with open(comment_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=4)
        return jsonify(comments)

    elif request.method == 'DELETE':
        # コメントを削除
        comments.pop(index)

        with open(comment_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=4)
        return jsonify(comments), 204


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
