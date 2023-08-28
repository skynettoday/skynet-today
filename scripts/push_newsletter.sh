digest_num=$1

digest_name=digest_$digest_num

rm "Last Week in AI News Planning - Past - $digest_num.csv"

git commit -am $digest_name
git push --set-upstream origin $digest_name

gh pr create --title "Digest $digest_num" --body "Digest $digest_num" --base master --head $digest_name --label "digest"
gh pr merge

git checkout master
git pull