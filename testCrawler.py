from crawler.dispatcher import selectWeb


print("=== web1 test ===")
result = selectWeb("constellation", ["2000","5","15"])
print(result)

print("=== web2 test ===")
result = selectWeb("name", ["王","小民"])
print(result)
