# export NODE_OPTIONS=--openssl-legacy-provider
from scripts.helpfull_scripts import deployAll, upgradeProxy 
from brownie import Box, BoxV2, BoxV3, BoxV4, Contract

def main():
    a = 5
    account, proxy_admin, proxy = deployAll()

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(a, {"from":account,"gas_limit": 1000000} )


    proxy_box = upgradeProxy(proxy_box, BoxV2, proxy, proxy_admin)
    proxy_box.increment({"from":account, "gas_limit": 1000000})
    print(proxy_box.retrieve())
    print(f"YESS, it should be {a+1}!!")
    print("what about next?")

    proxy_box = upgradeProxy(proxy_box, BoxV3, proxy, proxy_admin)
    proxy_box.multiply_10({"from":account, "gas_limit": 1000000})
    print(proxy_box.retrieve())    
    print(f"Yes! It should be {(a+1)*10}!!")

    print("Next should set our value to 3! Will it work?")
    proxy_box = upgradeProxy(proxy_box, BoxV4, proxy, proxy_admin)
    proxy_box.setTo3({"from":account, "gas_limit": 1000000})
    print(proxy_box.retrieve())  
    print("Yes!")

