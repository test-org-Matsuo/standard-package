"""
Excelファイルのシート判定と変換、Markdown雛形を作成するスクリプト

処理フロー:
1. Excelファイルを読み込み、全シート名を取得
2. シート名をh2セクションとした雛形Markdownファイルを作成
3. Excelファイルを1シートずつ別々のファイルに分ける
4. 各ファイルに画像や図形が含まれているかを判定
5. 図形・画像のあるExcelファイルは、画像化
6. 図形・画像のないExcelファイルは、AIによる直接テキスト抽出用として記録
"""
import sys
import os
import subprocess
from pathlib import Path
import xlwings as xw
import json


def has_images_in_sheet(sheet):
    """
    シートに画像が含まれているかチェック
    
    Args:
        sheet: xlwingsのシートオブジェクト
    
    Returns:
        bool: 画像が含まれている場合True
    """
    try:
        # シート内の図形（画像を含む）の数をチェック
        shapes_count = sheet.api.Shapes.Count
        return shapes_count > 0
    except:
        return False


def split_sheet_to_file(wb, sheet, output_dir, app):
    """
    シートを別ファイルとして保存
    
    Args:
        wb: 元のワークブック
        sheet: 分割するシート
        output_dir: 出力先ディレクトリ
        app: xlwingsのAppオブジェクト
    
    Returns:
        str: 保存したファイルのパス
    """
    sheet_name = sheet.name
    # ファイル名に使用できない文字を置換
    safe_sheet_name = sheet_name.replace('/', '_').replace('\\', '_').replace(':', '_')
    output_file = output_dir / f"{safe_sheet_name}.xlsx"
    
    # 新しいワークブックを作成
    new_wb = app.books.add()
    
    try:
        # シートをコピー
        sheet.api.Copy(Before=new_wb.sheets[0].api)
        
        # デフォルトシートを削除（複数シートがある場合のみ）
        if len(new_wb.sheets) > 1:
            try:
                new_wb.sheets[1].delete()
            except Exception as e:
                print(f"  警告: デフォルトシート削除失敗（無視して続行）: {e}")
        
        # ファイルを保存
        new_wb.save(str(output_file.absolute()))
        
        return str(output_file)
    
    finally:
        new_wb.close()


def convert_sheet_to_images(excel_file, sheet_name, output_dir, dpi=250, show_gridlines=False):
    """
    excel_to_images.pyを使用してシートを画像化する
    
    Args:
        excel_file: Excelファイルのパス
        sheet_name: シート名
        output_dir: 出力先ディレクトリ
        dpi: 解像度
        show_gridlines: グリッド線を表示するか（デフォルト: False）
    
    Returns:
        list: 生成された画像ファイルのパスリスト
    """
    # excel_to_images.pyのパスを取得
    script_dir = Path(__file__).parent.parent.parent / "xlsx-to-images" / "scripts"
    excel_to_images_script = script_dir / "excel_to_images.py"
    
    if not excel_to_images_script.exists():
        raise FileNotFoundError(f"excel_to_images.py が見つかりません: {excel_to_images_script}")
    
    # excel_to_images.pyを実行
    cmd = [
        sys.executable,
        str(excel_to_images_script),
        str(excel_file),
        "--output", str(output_dir),
        "--dpi", str(dpi),
        "--sheets", sheet_name,
        "--json"
    ]
    
    # グリッド線表示オプション
    if show_gridlines:
        cmd.append("--show-gridlines")
    
    result = subprocess.run(cmd, capture_output=True, text=False)
    
    if result.returncode != 0:
        stderr_text = result.stderr.decode('utf-8', errors='replace')
        raise RuntimeError(f"excel_to_images.py の実行に失敗しました: {stderr_text}")
    
    # JSON出力をパース（バイナリから直接デコード）
    try:
        stdout_text = result.stdout.decode('utf-8', errors='replace')
        # 最後の完全なJSONブロックを抽出
        json_start = stdout_text.rfind('\n{')
        if json_start == -1:
            json_start = stdout_text.rfind('{')
        if json_start == -1:
            raise ValueError("JSON出力が見つかりません")
        
        # 改行がある場合はスキップ
        if stdout_text[json_start] == '\n':
            json_start += 1
            
        json_end = stdout_text.rfind('}')
        if json_end == -1:
            raise ValueError("JSON出力が不完全です")
        
        json_text = stdout_text[json_start:json_end + 1]
        output_data = json.loads(json_text)
        if output_data.get('status') == 'success' and output_data.get('images'):
            return [img['image'] for img in output_data['images']]
        else:
            raise RuntimeError(f"画像変換に失敗しました: {output_data}")
    except (json.JSONDecodeError, ValueError) as e:
        raise RuntimeError(f"excel_to_images.py の出力をパースできませんでした: {e}")


def excel_to_images(excel_file, output_md=None, dpi=250, show_gridlines=False):
    """
    Excelファイルのシート判定と変換、Markdown雛形を作成する
    
    Args:
        excel_file: Excelファイルのパス
        output_md: 出力Markdownファイルのパス（Noneの場合は自動生成）
        dpi: 画像変換時の解像度（デフォルト: 250）
        show_gridlines: グリッド線を表示するか（デフォルト: False）
    
    Returns:
        dict: 変換結果の情報
    """
    excel_path = Path(excel_file)
    if not excel_path.exists():
        raise FileNotFoundError(f"Excelファイルが見つかりません: {excel_file}")
    
    # 出力ファイル名の設定
    if output_md is None:
        output_md = excel_path.parent / f"{excel_path.stem}.md"
    else:
        output_md = Path(output_md)
    
    # 作業用ディレクトリの作成
    work_dir = excel_path.parent / f"{excel_path.stem}_work"
    work_dir.mkdir(parents=True, exist_ok=True)
    
    # シート分割用ディレクトリ
    sheets_dir = work_dir / "sheets"
    sheets_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Excelファイルを変換中: {excel_file}")
    print(f"作業ディレクトリ: {work_dir}")
    
    # Excelを開く
    app = xw.App(visible=False)
    wb = app.books.open(str(excel_path.absolute()))
    
    try:
        # Step 1: シート情報を収集
        sheet_info = []
        print("\n=== Step 1: シート情報収集 ===")
        for sheet in wb.sheets:
            sheet_name = sheet.name
            has_images = has_images_in_sheet(sheet)
            sheet_info.append({
                'name': sheet_name,
                'has_images': has_images,
                'split_file': None,
                'images': []
            })
            print(f"シート '{sheet_name}': {'画像・図形あり' if has_images else '画像・図形なし'}")
        
        # Step 2: 雛形Markdownを作成
        print("\n=== Step 2: 雛形Markdown作成 ===")
        md_content = f"# {excel_path.stem}\n\n"
        
        for info in sheet_info:
            sheet_name = info['name']
            has_images = info['has_images']
            md_content += f"## {sheet_name}\n\n"
            
            # 画像・図形なしシートにはTODOコメントを追加
            if not has_images:
                md_content += f"<!-- TODO: シート '{sheet_name}' の内容をここに追加（ExcelをAIで読み取り） -->\n\n"
            else:
                # 画像・図形ありシートには画像参照を追加（後でStep 5で更新）
                md_content += f"<!-- IMAGES: シート '{sheet_name}' の画像をここに追加 -->\n\n"
        
        # 雛形を保存
        with open(output_md, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"雛形Markdown作成完了: {output_md}")
        
        # Step 3: シートを別ファイルに分割
        print("\n=== Step 3: シート分割 ===")
        for info in sheet_info:
            sheet_name = info['name']
            sheet = wb.sheets[sheet_name]
            
            print(f"シート '{sheet_name}' を分割中...")
            split_file = split_sheet_to_file(wb, sheet, sheets_dir, app)
            info['split_file'] = split_file
            print(f"  保存完了: {split_file}")
        
        # Step 4-5: 画像・図形ありシートを画像化
        print("\n=== Step 4-5: 画像・図形ありシートの画像化 ===")
        for info in sheet_info:
            sheet_name = info['name']
            has_images = info['has_images']
            split_file = info['split_file']
            
            if has_images:
                print(f"\nシート '{sheet_name}' を画像化中...")
                
                # 画像出力ディレクトリ
                safe_sheet_name = sheet_name.replace('/', '_').replace('\\', '_').replace(':', '_')
                images_dir = work_dir / f"{safe_sheet_name}_images"
                
                try:
                    image_files = convert_sheet_to_images(
                        split_file,
                        sheet_name,
                        str(images_dir),
                        dpi,
                        show_gridlines
                    )
                    print(f"  画像化完了: {len(image_files)}ファイル")
                    info['images'] = image_files
                except Exception as e:
                    error_msg = str(e).encode('utf-8', errors='replace').decode('utf-8')
                    print(f"  警告: 画像化に失敗しました: {error_msg}")
                    info['images'] = []
        
        # Step 5.5: 雛形Markdownに画像参照を追加
        print("\n=== Step 5.5: 画像参照の追加 ===")
        with open(output_md, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        for info in sheet_info:
            sheet_name = info['name']
            has_images = info['has_images']
            
            if has_images and info['images']:
                # プレースホルダーを検索
                placeholder = f"<!-- IMAGES: シート '{sheet_name}' の画像をここに追加 -->"
                
                # 画像参照を生成
                image_refs = []
                for img_path in info['images']:
                    # 相対パスを計算
                    rel_path = Path(img_path).relative_to(output_md.parent)
                    # パス区切り文字を/に統一し、<>で囲む
                    rel_path_str = str(rel_path).replace('\\', '/')
                    image_refs.append(f"![{sheet_name}](<{rel_path_str}>)")
                
                # プレースホルダーを画像参照に置き換え
                images_text = "\n\n".join(image_refs) + "\n"
                md_content = md_content.replace(placeholder, images_text)
                print(f"シート '{sheet_name}': {len(info['images'])}個の画像参照を追加")
        
        # 更新したMarkdownを保存
        with open(output_md, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # Step 6: 画像・図形なしシートの記録
        print("\n=== Step 6: 画像・図形なしシートの記録 ===")
        for info in sheet_info:
            sheet_name = info['name']
            has_images = info['has_images']
            
            if not has_images:
                print(f"シート '{sheet_name}' は画像・図形なし - AIによるテキスト抽出対象")
        
        # Step 7: メタ情報をJSONで保存
        print("\n=== Step 7: メタ情報保存 ===")
        meta_file = work_dir / "sheet_info.json"
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(sheet_info, f, ensure_ascii=False, indent=2)
        print(f"シート情報を保存: {meta_file}")
        
        print(f"\n変換完了: {output_md}")
        
        return {
            'markdown_file': str(output_md),
            'work_dir': str(work_dir),
            'sheet_info': sheet_info
        }
    
    finally:
        wb.close()
        app.quit()


def main():
    """
    メイン処理
    """
    if len(sys.argv) < 2:
        print("使用方法: python excel_to_markdown_with_images.py <Excelファイルパス> [出力Markdownファイルパス] [DPI] [--show-gridlines]")
        print("\n例:")
        print('  python excel_to_markdown_with_images.py "コーディング規約.xlsx"')
        print('  python excel_to_markdown_with_images.py "document.xlsx" "output.md" 250')
        print('  python excel_to_markdown_with_images.py "document.xlsx" "output.md" 250 --show-gridlines')
        sys.exit(1)
    
    excel_file = sys.argv[1]
    output_md = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
    dpi = 250
    show_gridlines = False
    
    # Parse remaining arguments
    for i in range(2, len(sys.argv)):
        arg = sys.argv[i]
        if arg == '--show-gridlines':
            show_gridlines = True
        elif arg.isdigit():
            dpi = int(arg)
    
    try:
        result = excel_to_images(excel_file, output_md, dpi, show_gridlines)
        print(f"\n[OK] 変換成功")
        print(f"  Markdownファイル: {result['markdown_file']}")
        print(f"  作業ディレクトリ: {result['work_dir']}")
        print(f"\n次のステップ:")
        print(f"  1. sheet_info.jsonで画像・図形なしシートを確認")
        print(f"  2. AIを使ってExcelファイルから直接テキストを抽出")
        print(f"  3. merge_markdown.pyを使ってマージ")
    except Exception as e:
        print(f"\n[ERROR] エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
