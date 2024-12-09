# dotmatrix_font

design and display dotmatrix font for pygame and Minecraft

ドットマトリクスフォントをデザインし、pygameとMinecraftで表示する。

![app window](images/designer.png)

## 注意

**「なつめもじ」フォントを利用しているが、再配布禁止のため、以下のページの一番下の＜＜「なつめもじ」をダウンロード＞＞というリンクからダウンロードすること。**

[あんずいろapricot×color  なつめもじ](http://www8.plala.or.jp/p_dolce/site3-5.html)

nm.zipを展開して得られたnatumemozi.ttfを、fontsフォルダにコピーして利用する。

## Python環境

Python 3.11.9で動作確認済み。

### pyenvがインストールされている場合

Python 3.11.9がない場合は、インストールする。

```bash
pyenv install 3.11.9
pyenv local 3.11.9
```

さらに、以下のコマンドでpygame-ceをインストールする。

```bash
pip install pygame-ce
```

### pyenvに加え、poetryもインストールされている場合

必要に応じて、以下のコマンドで環境を構築する。

```bash
pyenv install 3.11.9
pyenv local 3.11.9
poetry install
```

VS Codeの場合は、新しくターミナルを開けば、仮想環境が有効になるはず。
有効になっていない場合は、以下のコマンドで有効にする。

```bash
source .venv/bin/activate
```

あとは、VS Codeが使用するPythonインタープリターを、この仮想環境に設定する。
Pythonファイルを開いている状態で、ウィンドウの下部にPython 3.11.9 ('.venv': Poetry)と表示されていればOK。違う場合は、クリックして選択する。
![仮想環境の設定](images/vscode.png)

## 概要

- **designer.py**
    ドットマトリクスフォントをデザインするツール

以下、未実装

- **demo_pg.py**
    ドットマトリクスフォントを表示するデモコード
- **demo_mc.py**
    ドットマトリクスフォントをMinecraftで表示するデモコード

## フォントデザインツール　designer.py

**横（COLS、デフォルト5ドット）x縦（ROWS、デフォルト7ドット）のドットマトリクスフォントをデザインする。**

得られるものは、font.txtというファイル。
あるいは、起動時に読み込んだfont.txtの内容を一覧し、一部を編集／保存する使いかたもできる。

### ウィンドウ構成

上部にフォント一覧用の表示領域、左下にデザイン参照用領域（青色）、右下にデザイン編集用領域（赤色）を持つ。
表示領域は、横（DISPLAY_COLS、デフォルト16文字）ｘ縦（DISPLAY_ROWS、デフォルト6文字）の96文字で構成される。
wasdキーの操作で表示領域の中で青く表示される文字が移動し、選ばれた文字デザインが左下の参照領域に大きく表示される。
上下左右キーの操作で表示領域の中で赤く表示される文字が移動し、選ばれた文字デザインが右下の編集領域に大きく表示される。

### 操作概要

右下の編集領域で、各ドットをクリックすると、そのドットの状態が反転する。

鉛筆ボタンのクリック、あるいはEnterキーを押すと、編集領域のデザインが表示領域の赤色表示位置に書き込まれる。

緑色の右矢印ボタンのクリックで、参照領域のデザインが編集領域にコピーされる。

チェックボタンのクリックで、表示領域の全ての文字のデザインデータがfont.txtに保存される。

### フォントデータ

フォントデータはfont.txtに、00000,改行11111,改行 といった改行区切り形式で、96文字分が連続的に保存される。

起動時にfont.txtが存在しない場合は全て0で初期化して編集開始、
存在する場合は内容を読み込んで編集開始する。また、バックアップとしてfont.txt.bakを作成する。

現状のコードでも、例えば、8x8のフォントを扱うことは可能だが、font.txtのデータ形式が8x8以外だとエラーになる可能性がある。その場合は、font.txtファイルを削除して、再度designer.pyを起動することで初期化され、編集可能になる。

将来的には、ドットマトリクスの横x縦ドット数についてのデータをfont.txtの先頭に記述する予定。

例えば、5x7の場合は、

```json
[{"cols":5},{"rows":7}]
00000,
11111,
10101,
,,,
```

というような形式。これによって、任意のドット数のフォントデータを柔軟に扱えるようになる。ヘッダーのjson部分に収容文字数、コードの範囲、フォント名などを追加するかもしれない。
