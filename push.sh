if [ "$1" = "" ]
then
  echo "Please provide commit message"
  exit 0
fi

git add .
git commit -m "$1"
git push origin dev
