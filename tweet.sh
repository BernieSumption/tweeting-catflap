#usage tweet.sh "message" photofile

# This consumer key and token posts to @BernieTestAccnt. To generate a new one, go through
# this process (doesn't have to be on the same PC as the final program will run on)_
#
# "sudo easy_install twitter" then "twitter set foo". You'll be led through the OAuth
# dance. When you're authenticated, copy the first two lines from ~/twitter_oauth

curl -v \
    -F "consumer_token=uS6hO2sV6tDKIOeVjhnFnQ" \
    -F "consumer_secret=MEYTOS97VvlHX7K1rwHPEqVpTSqZ71HtvoK4sVuYk" \
    -F "oauth_token=1334844578-z3Ju3FUAQKZKogQnK7kbqngeeSQxX1wkeGwRiey" \
    -F "oauth_secret=HD1w0jh2x2nxAcgPI6Cux1SKbxI0VxaQYHvNZn8dGxQ" \
    -F "message=$1" \
    -F "key=a850e635a4d29d2f5b945b9f3fe01062" \
    -F "media=@$2" \
    http://api.twitpic.com/1/uploadAndPost.json