#!/bin/bash -ex

# Read variables
source config/env.sh

# IFSは、単語分割に使用されるフィールドのセパレータを指定する環境変数
# デフォルトでは空白文字、タブ文字、改行文字を含んでいる
SAVEIFS=$IFS
# 
# 改行やバックスペースを含むファイル名を正しく扱うため、IFSに改行とバックスペースを指定
# findコマンドで取得したファイル名をループ処理で扱う場合に、ファイル名内に空白文字が含まれている場合があるため
# 空白文字を含むファイル名などのテキストを正しく扱えるようになる
IFS=$(echo -en "\n\b")

# Change directory to DUMP_DIR
cd "${DUMP_DIR}"

# Process each file that matches PAGE_FILE_NAME
files=($(find . -name "${PAGE_FILE_NAME}"))
for file_path in "${files[@]}"; do  # Get the relative file path, base path, and page name
  relative_file_path=$(realpath --relative-to="${SCRIPT_DIR}" "${file_path}")
  base_path=$(dirname "${relative_file_path}")
  page_name=$(echo "${file_path}" | sed -e 's#/page.txt##' | sed -e 's#^\./##')
  # Change directory to SCRIPT_DIR
  cd "${SCRIPT_DIR}"

  attachments=""
  # Check if the attachments directory exists and process the file
  if [ -d "${base_path}/attachments" ]; then
    attachments=$(find ${base_path}/attachments -type f)
  fi
  cat "${relative_file_path}" | python3 "${CREATE_PAGE_SCRIPT_NAME}" "/${page_name}" "${attachments}"

  # Change directory back to DUMP_DIR
  cd "${DUMP_DIR}"
done
# d3diaryフォルダが存在する場合は、d3diaryの日誌も作成する
if [ -d "${D3DIARY_DIARY_DIR}" ]; then
  # Change directory to SCRIPT_DIR
  cd "${SCRIPT_DIR}"
  python3 "${CREATE_DIARY_SCRIPT_NAME}"
fi
# Reset IFS
IFS=$SAVEIFS
