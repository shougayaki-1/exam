import csv
import json
import os

def convert_csv_to_json(csv_filepath, subject_id, subject_title):
    """
    指定されたCSVファイルを読み込み、階層構造を持つJSONオブジェクトを構築して返す。
    """
    content_sets = []
    current_set = None

    try:
        with open(csv_filepath, mode='r', encoding='utf-8') as csvfile:
            # CSVのヘッダーを自動で認識
            reader = csv.DictReader(csvfile)
            
            for i, row in enumerate(reader):
                # 行番号 (デバッグ用)
                line_num = i + 2 
                
                row_type = row.get('row_type', '').strip().lower()

                if not row_type:
                    print(f"警告: {line_num}行目の 'row_type' が空です。この行はスキップされます。")
                    continue

                if row_type == 'set':
                    if current_set:
                        content_sets.append(current_set)
                    
                    # 必須項目チェック
                    if not all([row.get('set_id'), row.get('set_title')]):
                        print(f"警告: {line_num}行目の問題セットで 'set_id' または 'set_title' が不足しています。スキップします。")
                        current_set = None
                        continue

                    current_set = {
                        "id": row['set_id'].strip(),
                        "title": row['set_title'].strip(),
                        "description": row.get('set_description', '').strip(),
                        "isMath": row.get('is_math', 'false').strip().upper() == 'TRUE',
                        "questions": []
                    }
                elif row_type == 'question':
                    if not current_set:
                        print(f"警告: {line_num}行目の問題は、属する問題セット(set)が定義されていません。スキップします。")
                        continue
                    
                    question = {
                        "id": row.get('q_id', '').strip(),
                        "q_num": row.get('q_num', '').strip(),
                        "question_text": row.get('question_text', '').strip(),
                        "hint": row.get('hint', '').strip(),
                        "answer": row.get('answer', '').strip(),
                        "explanation": row.get('explanation', '').strip()
                    }
                    current_set['questions'].append(question)

            if current_set:
                content_sets.append(current_set)

    except FileNotFoundError:
        print(f"エラー: ファイル '{csv_filepath}' が見つかりません。")
        return None
    except Exception as e:
        print(f"エラー: ファイル処理中に予期せぬ問題が発生しました: {e}")
        return None

    # 最終的なJSON構造を構築
    json_data = {
        "id": subject_id,
        "title": subject_title,
        "contentSets": content_sets
    }
    
    return json_data

def main():
    """
    ユーザーとの対話を通じてCSVをJSONに変換するメインの処理。
    """
    print("--- CSV to JSON 変換スクリプト ---")
    print("`converter`フォルダ内のCSVファイルを、Webサイト用のJSONデータに変換します。\n")

    # 1. 入力CSVファイル名の取得
    csv_filename = input("変換したいCSVファイル名を入力してください (例: math.csv): ")
    
    # 2. 教科IDの取得
    subject_id = input("教科IDを入力してください (例: math): ")
    
    # 3. 教科名の取得
    subject_title = input("教科名を入力してください (例: 数学): ")

    print("\n--- 変換処理を開始します ---")

    # --- パスの設定 ---
    # このスクリプト(convert_csv_to_json.py)がある場所を基準にする
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 入力CSVのフルパス
    input_csv_path = os.path.join(script_dir, csv_filename)
    
    # 出力先ディレクトリのパス
    output_dir = os.path.join(script_dir, '..', '202509', 'data')
    
    # 出力JSONのファイル名
    output_json_filename = f"{subject_id}.json"
    
    # 出力JSONのフルパス
    output_json_path = os.path.join(output_dir, output_json_filename)

    # 出力先ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        print(f"出力先ディレクトリ '{output_dir}' が存在しないため、作成します。")
        os.makedirs(output_dir)

    # 変換を実行
    converted_data = convert_csv_to_json(input_csv_path, subject_id, subject_title)

    if converted_data:
        # JSONファイルに書き出し
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(converted_data, f, indent=2, ensure_ascii=False)
        
        print("\n--- 変換完了 ---")
        print(f"入力ファイル: {input_csv_path}")
        print(f"出力ファイル: {output_json_path}")
        print("正常に変換が完了しました。")
    else:
        print("\n--- 変換失敗 ---")
        print("エラーが発生したため、JSONファイルは生成されませんでした。")

if __name__ == '__main__':
    main()
    input("\n何かキーを押すと終了します...") # ユーザーが結果を確認できるように待機