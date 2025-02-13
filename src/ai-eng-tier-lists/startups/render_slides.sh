FILE_NAME=startups_tier_list
rm $FILE_NAME.html
rm $FILE_NAME.pdf
marp --allow-local-files --html --theme='dracula.css' $FILE_NAME.md $FILE_NAME.pdf
marp --pdf --allow-local-files --html --theme='dracula.css' $FILE_NAME.md $FILE_NAME.pdf
