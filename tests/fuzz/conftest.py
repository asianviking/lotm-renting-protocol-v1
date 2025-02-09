from textwrap import dedent

import boa
import pytest


@pytest.fixture(scope="session")
def accounts():
    _accounts = [boa.env.generate_address() for _ in range(10)]
    for account in _accounts:
        boa.env.set_balance(account, 10**21)
    return _accounts


@pytest.fixture(scope="session")
def owner():
    acc = boa.env.generate_address("owner")
    boa.env.eoa = acc
    boa.env.set_balance(acc, 10**21)
    return acc


@pytest.fixture(scope="session")
def nft_owner():
    acc = boa.env.generate_address("nft_owner")
    boa.env.set_balance(acc, 10**21)
    return acc


@pytest.fixture(scope="session")
def renter():
    acc = boa.env.generate_address("renter")
    boa.env.set_balance(acc, 10**21)
    return acc


@pytest.fixture(scope="session")
def nft_contract(owner):
    with boa.env.prank(owner):
        return boa.load("contracts/auxiliary/ERC721.vy")


@pytest.fixture(scope="session")
def ape_contract(owner):
    with boa.env.prank(owner):
        return boa.load("contracts/auxiliary/ERC20.vy", "APE", "APE", 18, 0)


@pytest.fixture(scope="session")
def delegation_registry_warm_contract():
    return boa.load("tests/stubs/DelegationRegistry.vy")


@pytest.fixture(scope="session")
def vault_contract_def():
    return boa.load_partial("contracts/Vault.vy")


@pytest.fixture(scope="session")
def renting_contract_def():
    return boa.load_partial("contracts/Renting.vy")


@pytest.fixture(scope="session")
def empty_contract_def():
    return boa.loads_partial(
        dedent(
            """
        dummy: uint256
     """
        )
    )


@pytest.fixture(scope="session")
def delegation_registry_mock():
    return boa.loads(
        dedent(
            """
    hot: HashMap[address, address]
    exp: HashMap[address, uint256]

    @external
    def setHotWallet(hot_wallet_address: address, expiration_timestamp: uint256, lock_hot_wallet_address: bool):
        self.hot[msg.sender] = hot_wallet_address
        self.exp[msg.sender] = expiration_timestamp if hot_wallet_address != empty(address) else 0

    @external
    def setExpirationTimestamp(expiration_timestamp: uint256):
        self.exp[msg.sender] = expiration_timestamp

    @view
    @external
    def getHotWallet(cold_wallet: address) -> address:
        return self.hot[cold_wallet] if self.exp[cold_wallet] > block.timestamp else empty(address)
     """
        )
    )


@pytest.fixture(scope="module")
def vault_contract(vault_contract_def):
    return vault_contract_def.deploy()


@pytest.fixture(scope="module")
def renting_contract(renting_contract_def, vault_contract, ape_contract, nft_contract, delegation_registry_mock):
    return renting_contract_def.deploy(vault_contract, ape_contract, nft_contract, delegation_registry_mock)
