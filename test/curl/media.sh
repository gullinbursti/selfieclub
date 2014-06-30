curl -v --request POST \
    -H 'Accept: application/json; indent=4' \
    "http://127.0.0.1:8000/media/" \
    --data-urlencode "club_id=40" \
    --data-urlencode "user_id=131820" \
    --data-urlencode "content_type=image/png" \
    --data-urlencode "file_name=test-image.png" \
    --data-urlencode "size=31231"

