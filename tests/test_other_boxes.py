from scripts.helpfull_scripts import deployAll,upgradeProxy
from brownie import Box, BoxV2, BoxV3, BoxV4, Contract 
import pytest


def test():
    a = 8
    account, proxy_admin, proxy = deployAll()
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(a,{"from":account,"gas_limit": 1000000})
    assert proxy_box.retrieve() == a

    account, proxy_admin, proxy, proxy_box = proxy_upgrade_V2(account, proxy_admin, proxy, proxy_box)
    assert proxy_box.retrieve() == a+1

    account, proxy_admin, proxy, proxy_box = proxy_upgrade_V3(account, proxy_admin, proxy, proxy_box)
    assert proxy_box.retrieve() == (a+1)*10

    account, proxy_admin, proxy, proxy_box = proxy_upgrade_V4(account, proxy_admin, proxy, proxy_box)
    assert proxy_box.retrieve() == 3


def proxy_upgrade_V2(account, proxy_admin, proxy, proxy_box):
    proxy_box = upgradeProxy(proxy_box, BoxV2, proxy, proxy_admin)
    proxy_box.increment({"from":account,"gas_limit": 1000000})
    return account, proxy_admin, proxy, proxy_box

def proxy_upgrade_V3(account, proxy_admin, proxy, proxy_box):
    proxy_box = upgradeProxy(proxy_box, BoxV3, proxy, proxy_admin)
    proxy_box.multiply_10({"from":account,"gas_limit": 1000000})
    return account, proxy_admin, proxy, proxy_box

def proxy_upgrade_V4(account, proxy_admin, proxy, proxy_box):
    proxy_box = upgradeProxy(proxy_box, BoxV4, proxy, proxy_admin)
    proxy_box.setTo3({"from":account,"gas_limit": 1000000})
    return account, proxy_admin, proxy, proxy_box    