#/bin/sh

echo Enter project name
read project_name

sed -i 's/<project_name>/$project_name' docker-compose.yml
sed -i 's/<project_name>/$project_name' README.md
mv src/project_name src/$project_name
