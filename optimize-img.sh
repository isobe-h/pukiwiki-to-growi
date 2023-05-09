#!/bin/bash -ex

source config/env.sh

extensions=("jpg" "jpeg" "JPG" "JPEG" "png" "PNG" "gif" "GIF")

function search_files() {
  local dir="$1"
  local ext="$2"

  for file in "$dir"/*; do
    if [[ -d "$file" ]]; then
      # If the file is a directory, recursively call the function
      search_files "$file" "$ext"
    elif [[ -f "$file" && "${file##*.}" == "$ext" ]]; then
      # If the file is a regular file and has the correct extension, run the script
      python3 "${SCRIPT_DIR}/${OPTIMIZE_SCRIPT_NAME}" "$file"
    fi
  done
}

for ext in "${extensions[@]}"
do
    # DUMP_DIR内を再帰的に探索し、すべての画像、gifを最適化
    if [[ -d "$DUMP_DIR" ]]; then
      search_files "$DUMP_DIR" "$ext"
    fi
    if [ -d "${D3DIARY_PHOTOS_PATH}" ]; then
        for file in "${D3DIARY_PHOTOS_PATH}"/*."$ext"
        do
            # d3diaryの場合、サムネイルが自動で作成されるため、頭に't_'がつくサムネイル画像は削除
            if [[ "$file" =~ ^.*t_.*$ ]]; then
                rm "$file"
                continue
            fi
            python3 "${SCRIPT_DIR}"/"${OPTIMIZE_SCRIPT_NAME}" "$file" 
        done
    fi
done
