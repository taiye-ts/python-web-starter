#/bin/sh

echo Enter project name
read project_name

declare -a files_to_sed=(
  README.md
  ./src/api.py
  ./src/project_name/api/urls.py
)
for entry in "${files_to_sed[@]}"
  do
    sed -i '' "s/project_name/$project_name/g" $entry
  done


mv src/project_name src/$project_name
