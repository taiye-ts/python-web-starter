#/bin/sh

echo Enter project name
read project_name

files_to_sed=($(find -E . -type f -regex "^.py"))
for entry in "${files_to_sed[@]}"
  do
    sed -i '' "s/project_name/$project_name/g" $entry
  done

sed -i '' "s/project_name/$project_name/g" README.md
mv src/project_name src/$project_name
