import json

with open("RPC2_responses.txt", "r") as f:
    contents = f.read().splitlines()
contents = [response for response in contents if response]

f = open("RPC2_responses_processed_success.csv", "a")

for entry in contents:
    method, response = entry.split('\t')
    response = json.loads(response)
    if not response["result"]:
        response = response["error"]
        continue
    elif response.get("params") is not None:
        response = response["params"]
    else:
        response = "Success"
    f.write(f'{method},"{response}"\n')
    print(method, response)

# print(contents)