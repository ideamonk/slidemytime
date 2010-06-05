import -window root -quality 50 foo.jpg
convert foo.jpg -quality 50  -thumbnail '160x100' _foo.jpg
password="R41yCXYTtpvf"

echo "at `date`  `curl -sF img=@foo.jpg -F thumb=@_foo.jpg -F passphrase=$password  http://127.0.0.1:8080/posthere`"
rm foo*

sleep 1

./$0
