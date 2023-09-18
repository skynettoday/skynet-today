set -e

digest_num=$1
digest_name=digest_$digest_num

# Make digest

git checkout master
git pull
git checkout -b digest_$digest_num

python csv2md.py -n=$digest_num

# Push changes

rm *.csv

git add *
git commit -am $digest_name
# git push --set-upstream origin $digest_name

# gh pr create --title "Digest $digest_num" --body "Digest $digest_num" --base master --head $digest_name --label "digest"
# gh pr merge --auto --merge --delete-branch "$digest_name"

# git checkout master
# git pull

# Generate socials

# python md2socials.py -n=$digest_num