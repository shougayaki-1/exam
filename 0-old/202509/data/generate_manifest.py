import os
import json

def generate_subjects_manifest(directory="."):
    """
    指定されたディレクトリ（このスクリプトがある場所）にある教科別JSONファイルをスキャンし、
    subjects.json（目次ファイル）を自動生成または更新する。
    """
    subjects = []
    
    # 目次ファイルへのパスを定義
    manifest_path = os.path.join(directory, 'subjects.json')
    
    existing_order = []
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            existing_subjects = json.load(f)
            # JSONが空でなければ順序を読み込む
            if isinstance(existing_subjects, list):
                existing_order = [s.get('id') for s in existing_subjects if s.get('id')]
    except (FileNotFoundError, json.JSONDecodeError):
        pass # ファイルが存在しないか空の場合は何もしない

    print(f"'{os.path.abspath(directory)}' ディレクトリをスキャン中...")
    
    for filename in os.listdir(directory):
        if not filename.endswith('.json') or filename == 'subjects.json':
            continue
            
        filepath = os.path.join(directory, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                print(f"  - ファイル '{filename}' をチェック中...")
                data = json.load(f)
                
                if "id" in data and "title" in data and "contentSets" in data:
                    subject_info = {
                        "id": data["id"],
                        "title": data["title"],
                        "icon": data.get("icon", "menu_book"),
                        "file": filename
                    }
                    subjects.append(subject_info)
                    print(f"    -> OK: 教科 '{data['title']}' を追加しました。")
                else:
                    print(f"    -> スキップ: '{filename}' は必要なキー(id, title, contentSets)が不足しています。")

        except (json.JSONDecodeError, KeyError) as e:
            print(f"    -> 警告: '{filename}' の読み込みに失敗しました: {e}。スキップします。")

    subjects.sort(key=lambda s: existing_order.index(s['id']) if s.get('id') in existing_order else float('inf'))

    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(subjects, f, indent=2, ensure_ascii=False)

    print("-" * 20)
    if subjects:
        print(f"'{manifest_path}' が正常に更新されました。{len(subjects)}個の教科が見つかりました。")
    else:
        print(f"'{manifest_path}' は更新されましたが、教科データファイルが見つかりませんでした。")

if __name__ == '__main__':
    # スクリプト自身の場所を基準に実行
    script_dir = os.path.dirname(os.path.abspath(__file__))
    generate_subjects_manifest(script_dir)