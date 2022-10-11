bash test.sh

read -p "press q to exit, ENTER to continue: " r
if [ $r == "q" ] 
then
    exit 0
fi

rm -r dist
python setup.py sdist
twine upload dist/* -u __token__
