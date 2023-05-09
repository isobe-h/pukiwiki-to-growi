#!/bin/bash -ex

# read configs
source config/env.sh
IGNORE_PAGES=("${IGNORE_PAGES[@]}")

cd "${PUKIWIKI_PAGE_DIR}"

for file_path in *.txt; do
  page_name=$(echo "${file_path}" | sed -e 's/\.txt$//' | sed -e 's/\(..\)/%\1/g' | nkf --url-input)
  # Ignore settings files and ignored pages
  if [[ $page_name =~ ^: || " ${IGNORE_PAGES[*]} " == *" $page_name "* ]]; then
    echo "Ignore: ${page_name}"
    continue
  fi
  page_dir_name=$(echo ${page_name} | sed -e 's#[^/]/$##g')
  mkdir -p "${DUMP_DIR}/${page_dir_name}"
  cp -p "${PUKIWIKI_PAGE_DIR}/${file_path}" "${DUMP_DIR}/${page_dir_name}/${PAGE_FILE_NAME}"
done

# dump attachments
cd "${PUKIWIKI_ATTACHMENTS_DIR}"
for file_path in *; do  
  page_name=$(echo "${file_path}" | sed -e 's/\(..\)/%\1/g' | nkf --url-input)
  page_dir_name=$(echo "${file_path}" | sed -e 's/_.*$//' | sed -e 's/\(..\)/%\1/g' | nkf --url-input)
  attachment_file_name=$(echo "${file_path}" | sed -e 's/^[^_]*_//g' | sed -e 's/\(..\)/%\1/g' | nkf --url-input)
  if [[ " ${IGNORE_PAGES[*]} " == *" $page_dir_name "* ]]; then
    continue
  fi
  # ignore settings files
  if [[ "${page_dir_name}" =~ ^: && "${page_dir_name}" != ":RenderAttaches" ]]; then
    continue
  fi
  # 拡張子がlog,txt,pdfのファイルは無視
  if [[ "${file_path}" =~ \.txt$ || "${file_path}" =~ \.log$ || "${file_path}" =~ \.pdf$ ]]; then
    continue
  fi
  # 拡張子がないファイルは無視
  if [[ ! "${attachment_file_name}" =~ \..*$ ]]; then
    continue
  fi
  # copy attachments
  # -p でタイムスタンプを保持
  mkdir -p "${DUMP_DIR}/${page_dir_name}/${ATTACHMENTS_DIR_NAME}"
  cp -p "${file_path}" "${DUMP_DIR}/${page_dir_name}/${ATTACHMENTS_DIR_NAME}/${attachment_file_name}"
done
