for file in *.py
do
  expand -t2 $file > tempfile
  mv tempfile $file
  sed 's/\r//' $file > tempfile
  mv tempfile $file
  echo "translated file $file"
done