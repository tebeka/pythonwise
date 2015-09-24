# Create empty orphan branch for code review

git checkout --orphan code-review
git rm -rf .
git ci --allow-empty -m 'Code review - nuke all'
git push --set-upstream origin code-review
