# 変数定義生成用プロンプトテンプレート

## 更新情報

| バージョン | 日付 | 内容 |
| :--- | :--- | :--- |
| v1.00.00 | 2026/03/06 | 新規作成 |

## 生成対象

PGM指示書(MD)の変数定義部分。

## プロンプトテンプレートに当てはめる値の抜粋条件

| 変数 | 抜粋条件 |
|:-----------|:------------|
| variable_definition | ソースコードから変数定義部分を抜粋して入力する。 |

### variable_definition の入力例

```text
/*----------------------------------------------------------------------------*/
/*  Define Include File                                                       */
/*----------------------------------------------------------------------------*/
#include "PS1Z000.h"
#include "PS1A100.h" 
#include "PS1A000.h"
#include "PS1A192.h"

EXEC SQL INCLUDE SQLCA.H;
EXEC SQL INCLUDE PS1Y001.h;
EXEC SQL INCLUDE cs100tprdco.h;
EXEC SQL INCLUDE cs100wlscal.h;

/*----------------------------------------------------------------------------*/
/*  Define Constant Variable                                                  */
/*----------------------------------------------------------------------------*/

#define   MIN_DAT            "19000101"     /* 最小日               */

EXEC SQL BEGIN DECLARE SECTION;
      static const char FLAG_NG[] = "0";           /* フラグ（××しない） */
      static const char FLAG_OK[] = "1";           /* フラグ（××する）   */

    static const char SF_1[]    = "1";           /* 1直 */
    static const char SF_2[]    = "2";           /* 2直 */
    static const char SF_3[]    = "3";           /* 3直 */

    static const char CRSCTDAT_BLANK[] = "        "; /* 実績計上日ブランク    */
    static const char BLANK_3[] = "   ";
EXEC SQL END DECLARE SECTION;

#define MAX_VHCCOUNT 99999
```

## 生成結果のチェック観点

- 出力例の形式で出ているか。

## 生成例

```text
## 変数定義

### [#include]句
1. ヘッダーファイル
	1. PS1Z000.h
	2. PS1A100.h
	3. PS1A000.h
	4. PS1A192.h
2. SQL用ヘッダーファイル
	1. SQLCA.H
	2. PS1Y001.h
	3. cs100tprdco.h
	4. cs100wlscal.h

### [#define]句
1. 定義
   1. 変数名：MIN_DAT 値："19000101"
   2. 変数名：MAX_VHCCOUNT 値：99999
2. SQL用定義
   1. 変数名：FLAG_NG 値："0"
   2. 変数名：FLAG_OK 値："1"
   3. 変数名：SF_1 値："1"
   4. 変数名：SF_2 値："2"
   5. 変数名：SF_3 値："3"
   6. 変数名：CRSCTDAT_BLANK 値："        "
   7. 変数名：BLANK_3 値："   "
```

