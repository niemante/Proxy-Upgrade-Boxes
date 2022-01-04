from scripts.helpfull_scripts import deployAll
from brownie import Box, Contract 

def test_proxy_delegates_calls():
    account, proxy_admin, proxy = deployAll()
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    assert proxy_box.retrieve() == 0
    proxy_box.store(1,{"from":account})
    assert proxy_box.retrieve() == 1

