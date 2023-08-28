digest_num=$1

git checkout master
git pull
git checkout -b digest_$digest_num

python csv2md.py -n=$digest_num

python md2socials.py -n=$digest_num