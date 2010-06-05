import -window root -quality 50 foo.jpg
convert foo.jpg -quality 50  -thumbnail '160x100' _foo.jpg

password="x5VpJWYAUte2" # passphrase on server
delay=300 # 5 Minutes
server="http://127.0.0.1:8080/posthere"

echo "at `date`  `curl -sF img=@foo.jpg -F thumb=@_foo.jpg -F passphrase=$password  $server`"
rm foo.jpg _foo.jpg
sleep $delay
./$0 &
