import urllib3


def main(event, context):
    http = urllib3.PoolManager()
    res = http.request("GET", "https://httpbin.org/get")

    data = res.data.decode('utf-8')
    print(f"Request status: {res.status}")


main(None, None)
