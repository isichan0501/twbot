import requests, json



APIKey = 'HPQjg2cyfY2KhkyAjJftsv9qJTtuZU'
#sof07c2WBbKelzR2rJeK3vuPIg0L0h
#uaMZWvWeMAnuiZGrRFUtcTNSGuH8yh
#RPJdA9gqP8uMV0XExCMlCMdvSZb0rG
#mR8mYzz4blIdc71sKTnMKWDFhioKw0
#PuaVUbp3pkT3rSsuvuJNCH4NWTrILP
#PmwsDB2zVcVJNMWC4QeuaWYB84ZhKT

res = json.loads(requests.get(f"http://smspva.com/priemnik.php?metod=get_balance&service=opt4&apikey={APIKey}").text)

print(res)
import pdb;pdb.set_trace()
print(res)