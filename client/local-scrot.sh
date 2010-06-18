scrot foo.jpg -q 50 -t 10

password="VRuHUBTgdeDP" # passphrase on server
delay=300 # 5 Minutes
server="http://127.0.0.1:8080/posthere"

echo "at `date`  `curl -sF img=@foo.jpg -F thumb=@foo-thumb.jpg -F passphrase=$password  $server`"
rm foo.jpg foo-thumb.jpg
sleep $delay
./$0 &
