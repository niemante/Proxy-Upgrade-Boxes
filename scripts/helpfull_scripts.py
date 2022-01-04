from brownie import network, config, accounts, Contract, Box, ProxyAdmin, TransparentUpgradeableProxy
import eth_utils
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat","development","ganache"]

def get_account(index = None, id = None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None             

def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)

def upgrade(
    account,
    proxy,
    new_implementation_address,
    proxy_admin_contract = None,
    initializer = None,
    *args
):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encoded_function_call,
                {"from":account}
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address, new_implementation_address, {"from":account}
            )
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(
                new_implementation_address, encoded_function_call, {"from":account}
            )
        else:
            transaction = proxy.upgradeTo(new_implementation_address, {"from":account})
    return transaction

def upgradeProxy(proxy_box, contract, proxy, proxy_admin):
    account = get_account()
    proxy_address = proxy_box.address
    new_version = contract.deploy({"from":account,"gas_limit": 1000000}) # , publish_source = True
    upgrade_transaction = upgrade(  # this to func
        account, 
        proxy, 
        new_version.address, 
        proxy_admin_contract = proxy_admin,
        )    
    upgrade_transaction.wait(1)     
    print("Proxy has been updated") 
    proxy_box = Contract.from_abi(f"{contract}", proxy.address, contract.abi) 
    return proxy_box

def deployAll():
    account = get_account()
    # create func deploy all to make it easy
    box = Box.deploy({"from":account}) #, publish_source = True
    proxy_admin = ProxyAdmin.deploy({"from":account,"gas_limit": 1000000}) #, publish_source = True 
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from":account,"gas_limit": 1000000}, 
    )
    return account, proxy_admin, proxy
