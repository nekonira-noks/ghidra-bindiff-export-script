# ghidra-bindiff-export-script

Ghidra Bindiff Export Script は、Ghidra のバイナリ差分解析（Bindiff）を補助し、結果のエクスポートなどを自動化するためのスクリプト群です。
ファームウェアを展開した際のファイルシステムのディレクトリ構成を保持したまま，バイナリファイルをGhidraで解析し，Binexport形式にエクスポートするのに特化しています．

## 概要

このリポジトリには、Ghidra の Python スクリプト（Jython）として動作する `ExportToBinexport.py` が含まれています。  
主に Ghidra を活用して、解析対象バイナリを BinDiff で利用できる BinExport 形式にエクスポートする処理を自動化できます。

## スクリプト

### ExportToBinexport.py

- **目的**: Ghidra 上で開いているバイナリに対し、BinExport exporter の自動検索と出力ディレクトリの生成を行う。
- **主な処理手順**:
  1. **引数取得**: スクリプト実行時に出力先ディレクトリとファームウェア名を引数で受け取る。
  2. **現在開いているプログラム取得**: Ghidra API の `getCurrentProgram()` を利用。
  3. **出力ディレクトリ作成**: 引数情報を元に、ファームウェアごとのディレクトリを作成。
  4. **Exporter 検索**: 利用可能な Exporter 一覧から "BinExport" を含む Exporter を自動選択。
  5. **エラーハンドリング**: 引数不足やExporter未検出など、状況に応じてエラー出力。

- **主な利用API/クラス**:
  - `ghidra.app.util.exporter.ExporterLocator`
  - `ghidra.util.task.ConsoleTaskMonitor`
  - Ghidra script API（`getCurrentProgram`, `getScriptArgs`, `println`, `printerr` など）

## 使い方

### 1. スクリプトの設置

1. このリポジトリをクローンまたはダウンロード
2. `ExportToBinexport.py` を Ghidra スクリプトディレクトリに配置 わからなければ，Ghidraのマニュアルをみて

### 2. Ghidra での実行手順

1. Ghidra でターゲットバイナリを開く
2. 「Script Manager」から本スクリプトを選択
3. 以下の引数を指定してスクリプトを実行
   - **第1引数**: Binexportされたファイルを保存するディレクトリ

#### 例（ヘッドレス実行時）

```
analyzeHeadless <プロジェクトディレクトリ> <プロジェクト名> -import <バイナリファイル> -postScript ExportToBinexport.py <出力ディレクトリ> 
```

### 3. 出力

- 指定されたディレクトリ配下に、ファームウェアごとのサブディレクトリが自動生成されます。
- BinExport exporter が見つかれば、その情報が表示されます。
- Exporterが見つからない場合はエラーとなります（BinExport 拡張のインストール要）。

## 前提・依存

- Ghidra 
- BinExport 拡張（https://github.com/google/binexport）
- Ghidra の Python スクリプト実行環境（Jython）

## トラブルシューティング

- **Exporter が見つからない**
  - BinExport 拡張がインストール済みか確認してください。
  - Ghidra の「ファイル > Tool Plugins」から Extensions の有効化状況を確認。

- **ディレクトリ作成エラー**
  - 出力先ディレクトリへの書き込み権限があるか確認してください。

## ライセンス

このリポジトリは MIT ライセンスです。詳細は `LICENSE` を参照してください。

## 貢献・お問い合わせ

Issue や Pull Request を歓迎します。ご質問やバグ報告もお気軽にどうぞ。

---
