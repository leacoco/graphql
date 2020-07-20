TOKEN=${GITHUB_TOKEN}

WORKING_PAYLOAD=" \
 {\"query\": \
    \"query { \
        viewer { \
          login \
        } \
        rateLimit { \
          cost \
          remaining \
        } \
      }\"
  } \
"

REPO_PAYLOAD=" \
 {\"query\": \
    \"query { \
        viewer { \
          login \
          name \
          repositories(last: 50) { \
            nodes { \
              name \
            } \
          } \
        } \
        rateLimit { \
          cost \
          remaining \
        } \
      }\"
  } \
"
# curl -H "Authorization: bearer $TOKEN" -X POST -d " \
#  { \
#    \"query\": \"query { viewer { login }}\" \
#  } \
# " https://api.github.com/graphql

result=$(curl -s -H "Authorization: bearer $TOKEN" -X POST -H "Content-Type: application/json" -d "$REPO_PAYLOAD" https://api.github.com/graphql)

echo $result | jq .data
