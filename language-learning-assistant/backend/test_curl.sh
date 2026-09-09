# Test curl command for MP3 upload to Salad storage
curl -X PUT \
  "https://storage-api.salad.com/organizations/$SALAD_ORGANIZATION_NAME/files/audio/test.mp3" \
  --header "Salad-Api-Key: $SALAD_API_KEY" \
  --form 'mimeType="audio/mpeg"' \
  --form 'file=@./videos/DjxgpzIeiws.mp3' \
  --form 'sign=true' \
  --form 'signatureExp=259200'