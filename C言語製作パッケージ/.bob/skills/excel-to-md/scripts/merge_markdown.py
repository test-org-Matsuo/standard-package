"""
抽出したMarkdownコンテンツを雛形Markdownファイルにマージするスクリプト

使用方法:
  python merge_markdown.py <雛形Markdownファイル> <シート名> <抽出Markdownファイル>
"""
import sys
from pathlib import Path


def merge_markdown(template_md, sheet_name, content_md):
    """
    抽出したMarkdownコンテンツを雛形にマージする
    
    Args:
        template_md: 雛形Markdownファイルのパス
        sheet_name: マージ対象のシート名
        content_md: 抽出したMarkdownコンテンツファイルのパス
    
    Returns:
        bool: マージ成功フラグ
    """
    template_path = Path(template_md)
    content_path = Path(content_md)
    
    if not template_path.exists():
        raise FileNotFoundError(f"雛形ファイルが見つかりません: {template_md}")
    
    if not content_path.exists():
        raise FileNotFoundError(f"コンテンツファイルが見つかりません: {content_md}")
    
    # 雛形ファイルを読み込む
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # 抽出コンテンツを読み込む
    with open(content_path, 'r', encoding='utf-8') as f:
        extracted_content = f.read()
    
    # 該当セクションを見つける
    section_header = f"## {sheet_name}\n\n"
    
    if section_header not in template_content:
        print(f"警告: シート '{sheet_name}' のセクションが見つかりません")
        return False
    
    # セクションヘッダーの位置を見つける
    header_pos = template_content.find(section_header)
    content_start = header_pos + len(section_header)
    
    # 次のセクションヘッダーまたはファイル末尾を見つける
    next_section_pos = template_content.find("\n## ", content_start)
    
    # セクション内のコンテンツを取得
    if next_section_pos == -1:
        section_content = template_content[content_start:]
    else:
        section_content = template_content[content_start:next_section_pos]
    
    # TODOコメントを探す
    todo_comment = f"<!-- TODO: シート '{sheet_name}' の内容をここに追加（ExcelをAIで読み取り） -->"
    new_content = template_content  # 未代入によるUnboundLocalErrorを防ぐフォールバック
    
    if todo_comment in section_content:
        # TODOコメントを抽出コンテンツで置換
        new_section_content = section_content.replace(todo_comment, extracted_content)
        
        if next_section_pos == -1:
            new_content = template_content[:content_start] + new_section_content
        else:
            new_content = template_content[:content_start] + new_section_content + template_content[next_section_pos:]
    else:
        # TODOコメントがない場合は、画像参照の後に追加
        # 画像参照行を探す（![シート名](...)の形式）
        image_ref_pattern = f"![{sheet_name}]("
        if image_ref_pattern in section_content:
            # 画像参照行の後に改行を追加してコンテンツを挿入
            lines = section_content.split('\n')
            new_lines = []
            inserted = False
            
            for line in lines:
                new_lines.append(line)
                if image_ref_pattern in line and not inserted:
                    # 画像参照の後に空行と抽出コンテンツを追加
                    new_lines.append('')
                    new_lines.append(extracted_content.rstrip())
                    inserted = True
            
            new_section_content = '\n'.join(new_lines)
            
            if next_section_pos == -1:
                new_content = template_content[:content_start] + new_section_content + '\n\n'
            else:
                new_content = template_content[:content_start] + new_section_content + '\n' + template_content[next_section_pos:]
        else:
            # 画像参照もない場合は、既存コンテンツの確認
            existing_content = section_content.strip()
            if not existing_content:
                # 空の場合は追加
                if next_section_pos == -1:
                    new_content = template_content[:content_start] + extracted_content + "\n\n"
                else:
                    new_content = template_content[:content_start] + extracted_content + "\n" + template_content[next_section_pos:]
            else:
                # 既存コンテンツがある場合は確認
                print(f"警告: シート '{sheet_name}' には既にコンテンツがあります")
                print("上書きしますか? (y/n): ", end='')
                response = input().strip().lower()
                if response != 'y':
                    print("マージをキャンセルしました")
                    return False
                if next_section_pos == -1:
                    new_content = template_content[:content_start] + extracted_content + "\n\n"
                else:
                    new_content = template_content[:content_start] + extracted_content + "\n" + template_content[next_section_pos:]
    
    # ファイルに書き込む
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"[OK] シート '{sheet_name}' のコンテンツをマージしました")
    return True


def main():
    """
    メイン処理
    """
    if len(sys.argv) < 4:
        print("使用方法: python merge_markdown.py <雛形Markdownファイル> <シート名> <抽出Markdownファイル>")
        print("\n例:")
        print('  python merge_markdown.py "コーディング規約.md" "目次" "目次_extracted.md"')
        sys.exit(1)
    
    template_md = sys.argv[1]
    sheet_name = sys.argv[2]
    content_md = sys.argv[3]
    
    try:
        success = merge_markdown(template_md, sheet_name, content_md)
        if success:
            print(f"\n[OK] マージ完了: {template_md}")
        else:
            sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
