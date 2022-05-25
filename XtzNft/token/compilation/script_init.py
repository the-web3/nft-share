import smartpy as sp


TZIP16_Metadata_Base = {
    "name"          : "SmartPy FA1.2 Token Template",
    "description"   : "Example Template for an FA1.2 Contract from SmartPy",
    "authors"       : [
        "SmartPy Dev Team <email@domain.com>"
    ],
    "homepage"      : "https://smartpy.io",
    "interfaces"    : [
        "TZIP-007-2021-04-17",
        "TZIP-016-2021-04-17"
    ],
}

class FA12_Error:
    def make(s): return ("FA1.2_" + s)
    NotAdmin                        = make("NotAdmin")
    InsufficientBalance             = make("InsufficientBalance")
    UnsafeAllowanceChange           = make("UnsafeAllowanceChange")
    Paused                          = make("Paused")
    NotAllowed                      = make("NotAllowed")


class FA12_config:
    def __init__(
        self,
        support_upgradable_metadata         = False,
        use_token_metadata_offchain_view    = True,
    ):
        self.support_upgradable_metadata = support_upgradable_metadata
        self.use_token_metadata_offchain_view = use_token_metadata_offchain_view


class FA12_common:
    def normalize_metadata(self, metadata):
        for key in metadata:
            metadata[key] = sp.utils.bytes_of_string(metadata[key])
        return metadata


class FA12_core(sp.Contract, FA12_common):
    def __init__(self, config, **extra_storage):
        self.config = config

        self.init(
            balances = sp.big_map(tvalue = sp.TRecord(approvals = sp.TMap(sp.TAddress, sp.TNat), balance = sp.TNat)),
            totalSupply = 0,
            **extra_storage
        )

    @sp.entry_point
    def transfer(self, params):
        sp.set_type(params, sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value"))))
        sp.verify(self.is_administrator(sp.sender) |
            (~self.is_paused() &
                ((params.from_ == sp.sender) |
                 (self.data.balances[params.from_].approvals[sp.sender] >= params.value))), FA12_Error.NotAllowed)
        self.addAddressIfNecessary(params.from_)
        self.addAddressIfNecessary(params.to_)
        sp.verify(self.data.balances[params.from_].balance >= params.value, FA12_Error.InsufficientBalance)
        self.data.balances[params.from_].balance = sp.as_nat(self.data.balances[params.from_].balance - params.value)
        self.data.balances[params.to_].balance += params.value
        sp.if (params.from_ != sp.sender) & (~self.is_administrator(sp.sender)):
            self.data.balances[params.from_].approvals[sp.sender] = sp.as_nat(self.data.balances[params.from_].approvals[sp.sender] - params.value)

    @sp.entry_point
    def approve(self, params):
        sp.set_type(params, sp.TRecord(spender = sp.TAddress, value = sp.TNat).layout(("spender", "value")))
        self.addAddressIfNecessary(sp.sender)
        sp.verify(~self.is_paused(), FA12_Error.Paused)
        alreadyApproved = self.data.balances[sp.sender].approvals.get(params.spender, 0)
        sp.verify((alreadyApproved == 0) | (params.value == 0), FA12_Error.UnsafeAllowanceChange)
        self.data.balances[sp.sender].approvals[params.spender] = params.value

    def addAddressIfNecessary(self, address):
        sp.if ~ self.data.balances.contains(address):
            self.data.balances[address] = sp.record(balance = 0, approvals = {})

    @sp.utils.view(sp.TNat)
    def getBalance(self, params):
        sp.if self.data.balances.contains(params):
            sp.result(self.data.balances[params].balance)
        sp.else:
            sp.result(sp.nat(0))

    @sp.utils.view(sp.TNat)
    def getAllowance(self, params):
        sp.if self.data.balances.contains(params.owner):
            sp.result(self.data.balances[params.owner].approvals.get(params.spender, 0))
        sp.else:
            sp.result(sp.nat(0))

    @sp.utils.view(sp.TNat)
    def getTotalSupply(self, params):
        sp.set_type(params, sp.TUnit)
        sp.result(self.data.totalSupply)

    def is_paused(self):
        return sp.bool(False)

    def is_administrator(self, sender):
        return sp.bool(False)


class FA12_mint_burn(FA12_core):
    @sp.entry_point
    def mint(self, params):
        sp.set_type(params, sp.TRecord(address = sp.TAddress, value = sp.TNat))
        sp.verify(self.is_administrator(sp.sender), FA12_Error.NotAdmin)
        self.addAddressIfNecessary(params.address)
        self.data.balances[params.address].balance += params.value
        self.data.totalSupply += params.value

    @sp.entry_point
    def burn(self, params):
        sp.set_type(params, sp.TRecord(address = sp.TAddress, value = sp.TNat))
        sp.verify(self.is_administrator(sp.sender), FA12_Error.NotAdmin)
        sp.verify(self.data.balances[params.address].balance >= params.value, FA12_Error.InsufficientBalance)
        self.data.balances[params.address].balance = sp.as_nat(self.data.balances[params.address].balance - params.value)
        self.data.totalSupply = sp.as_nat(self.data.totalSupply - params.value)


class FA12_administrator(FA12_core):
    def is_administrator(self, sender):
        return sender == self.data.administrator

    @sp.entry_point
    def setAdministrator(self, params):
        sp.set_type(params, sp.TAddress)
        sp.verify(self.is_administrator(sp.sender), FA12_Error.NotAdmin)
        self.data.administrator = params

    @sp.utils.view(sp.TAddress)
    def getAdministrator(self, params):
        sp.set_type(params, sp.TUnit)
        sp.result(self.data.administrator)


class FA12_pause(FA12_core):
    def is_paused(self):
        return self.data.paused

    @sp.entry_point
    def setPause(self, params):
        sp.set_type(params, sp.TBool)
        sp.verify(self.is_administrator(sp.sender), FA12_Error.NotAdmin)
        self.data.paused = params


class FA12_token_metadata(FA12_core):
    def set_token_metadata(self, metadata):
        self.update_initial_storage(
            token_metadata = sp.big_map(
                {
                    0: sp.record(token_id = 0, token_info = self.normalize_metadata(metadata))
                },
                tkey = sp.TNat,
                tvalue = sp.TRecord(token_id = sp.TNat, token_info = sp.TMap(sp.TString, sp.TBytes))
            )
        )


class FA12_contract_metadata(FA12_core):
    def generate_tzip16_metadata(self):
        views = []

        def token_metadata(self, token_id):
            sp.set_type(token_id, sp.TNat)
            sp.result(self.data.token_metadata[token_id])

        if self.usingTokenMetadata and self.config.use_token_metadata_offchain_view:
            self.token_metadata = sp.offchain_view(pure = True, doc = "Get Token Metadata")(token_metadata)
            views += [self.token_metadata]

        metadata = {
            **TZIP16_Metadata_Base,
            "views"         : views
        }
        self.init_metadata("metadata", metadata)

    def set_contract_metadata(self, metadata):
        self.update_initial_storage(
            metadata = sp.big_map(self.normalize_metadata(metadata))
        )

        if self.config.support_upgradable_metadata:
            def update_metadata(self, key, value):
                sp.verify(self.is_administrator(sp.sender), FA12_Error.NotAdmin)
                self.data.metadata[key] = value
            self.update_metadata = sp.entry_point(update_metadata)

class FA12(
    FA12_mint_burn,
    FA12_administrator,
    FA12_pause,
    FA12_token_metadata,
    FA12_contract_metadata,
    FA12_core
):
    def __init__(self, admin, config, token_metadata = None, contract_metadata = None):
        FA12_core.__init__(self, config, paused = False, administrator = admin)

        if token_metadata is None and contract_metadata is None:
            raise Exception(
            """\n
                Contract must contain at least of the following:
                    \t- TZIP-016 %metadata big-map,
                    \t- Token-specific-metadata through the %token_metadata big-map

                More info: https://gitlab.com/tzip/tzip/blob/master/proposals/tzip-7/tzip-7.md#token-metadata
            """
            )

        self.usingTokenMetadata = False
        if token_metadata is not None:
            self.usingTokenMetadata = True
            self.set_token_metadata(token_metadata)
        if contract_metadata is not None:
            self.set_contract_metadata(contract_metadata)
        self.generate_tzip16_metadata()


class Viewer(sp.Contract):
    def __init__(self, t):
        self.init(last = sp.none)
        self.init_type(sp.TRecord(last = sp.TOption(t)))
    @sp.entry_point
    def target(self, params):
        self.data.last = sp.some(params)



class TestOffchainView(sp.Contract):
    def __init__(self, f):
        self.f = f.f
        self.init(result = sp.none)

    @sp.entry_point
    def compute(self, data, params):
        b = sp.bind_block()
        with b:
            self.f(sp.record(data = data), params)
        self.data.result = sp.some(b.value)


if "templates" not in __name__:
    @sp.add_test(name = "FA12")
    def test():
        scenario = sp.test_scenario()
        scenario.h1("FA1.2 template - Fungible assets")

        scenario.table_of_contents()

        # sp.test_account generates ED25519 key-pairs deterministically:
        admin = sp.test_account("Administrator")
        alice = sp.test_account("Alice")
        bob   = sp.test_account("Robert")

        # Let's display the accounts:
        scenario.h1("Accounts")
        scenario.show([admin, alice, bob])

        scenario.h1("Contract")
        token_metadata = {
            "decimals"    : "18",               # Mandatory by the spec
            "name"        : "My Great Token",   # Recommended
            "symbol"      : "MGT",              # Recommended
            "icon"        : 'https://smartpy.io/static/img/logo-only.svg'
        }
        contract_metadata = {
            "" : "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
        }
        c1 = FA12(
            admin.address,
            config              = FA12_config(support_upgradable_metadata = True),
            token_metadata      = token_metadata,
            contract_metadata   = contract_metadata
        )
        scenario += c1

        scenario.h1("Offchain view - token_metadata")
        offchainViewTester = TestOffchainView(c1.token_metadata)
        scenario.register(offchainViewTester)
        offchainViewTester.compute(data = c1.data, params = 0)
        scenario.verify_equal(
            offchainViewTester.data.result,
            sp.some(
                sp.record(
                    token_id = 0,
                    token_info = sp.map({
                        "decimals"    : sp.utils.bytes_of_string("18"),
                        "name"        : sp.utils.bytes_of_string("My Great Token"),
                        "symbol"      : sp.utils.bytes_of_string("MGT"),
                        "icon"        : sp.utils.bytes_of_string('https://smartpy.io/static/img/logo-only.svg')
                    })
                )
            )
        )

        scenario.h1("Attempt to update metadata")
        scenario.verify(
            c1.data.metadata[""] == sp.utils.bytes_of_string("ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd")
        )
        c1.update_metadata(key = "", value = sp.bytes("0x00")).run(sender = admin)
        scenario.verify(c1.data.metadata[""] == sp.bytes("0x00"))

        scenario.h1("Entry points")
        scenario.h2("Admin mints a few coins")
        c1.mint(address = alice.address, value = 12).run(sender = admin)
        c1.mint(address = alice.address, value = 3).run(sender = admin)
        c1.mint(address = alice.address, value = 3).run(sender = admin)
        scenario.h2("Alice transfers to Bob")
        c1.transfer(from_ = alice.address, to_ = bob.address, value = 4).run(sender = alice)
        scenario.verify(c1.data.balances[alice.address].balance == 14)
        scenario.h2("Bob tries to transfer from Alice but he doesn't have her approval")
        c1.transfer(from_ = alice.address, to_ = bob.address, value = 4).run(sender = bob, valid = False)
        scenario.h2("Alice approves Bob and Bob transfers")
        c1.approve(spender = bob.address, value = 5).run(sender = alice)
        c1.transfer(from_ = alice.address, to_ = bob.address, value = 4).run(sender = bob)
        scenario.h2("Bob tries to over-transfer from Alice")
        c1.transfer(from_ = alice.address, to_ = bob.address, value = 4).run(sender = bob, valid = False)
        scenario.h2("Admin burns Bob token")
        c1.burn(address = bob.address, value = 1).run(sender = admin)
        scenario.verify(c1.data.balances[alice.address].balance == 10)
        scenario.h2("Alice tries to burn Bob token")
        c1.burn(address = bob.address, value = 1).run(sender = alice, valid = False)
        scenario.h2("Admin pauses the contract and Alice cannot transfer anymore")
        c1.setPause(True).run(sender = admin)
        c1.transfer(from_ = alice.address, to_ = bob.address, value = 4).run(sender = alice, valid = False)
        scenario.verify(c1.data.balances[alice.address].balance == 10)
        scenario.h2("Admin transfers while on pause")
        c1.transfer(from_ = alice.address, to_ = bob.address, value = 1).run(sender = admin)
        scenario.h2("Admin unpauses the contract and transfers are allowed")
        c1.setPause(False).run(sender = admin)
        scenario.verify(c1.data.balances[alice.address].balance == 9)
        c1.transfer(from_ = alice.address, to_ = bob.address, value = 1).run(sender = alice)

        scenario.verify(c1.data.totalSupply == 17)
        scenario.verify(c1.data.balances[alice.address].balance == 8)
        scenario.verify(c1.data.balances[bob.address].balance == 9)

        scenario.h1("Views")
        scenario.h2("Balance")
        view_balance = Viewer(sp.TNat)
        scenario += view_balance
        c1.getBalance((alice.address, view_balance.typed.target))
        scenario.verify_equal(view_balance.data.last, sp.some(8))

        scenario.h2("Administrator")
        view_administrator = Viewer(sp.TAddress)
        scenario += view_administrator
        c1.getAdministrator((sp.unit, view_administrator.typed.target))
        scenario.verify_equal(view_administrator.data.last, sp.some(admin.address))

        scenario.h2("Total Supply")
        view_totalSupply = Viewer(sp.TNat)
        scenario += view_totalSupply
        c1.getTotalSupply((sp.unit, view_totalSupply.typed.target))
        scenario.verify_equal(view_totalSupply.data.last, sp.some(17))

        scenario.h2("Allowance")
        view_allowance = Viewer(sp.TNat)
        scenario += view_allowance
        c1.getAllowance((sp.record(owner = alice.address, spender = bob.address), view_allowance.typed.target))
        scenario.verify_equal(view_allowance.data.last, sp.some(1))

    sp.add_compilation_target(
        "WenwoToken",
        FA12(
            admin   = sp.address("tz1iJzB6WsHiSd9TJgmQHNXwc4eyRs9GvfJj"),
            config  = FA12_config(
                support_upgradable_metadata         = True,
                use_token_metadata_offchain_view    = True
            ),
            token_metadata = {
                "decimals"    : "18",
                "name"        : "WenwoToken",
                "symbol"      : "WWT",
                "icon"        : 'https://smartpy.io/static/img/logo-only.svg'
            },
            contract_metadata = {
                "" : "ipfs://QmaiAUj1FFNGYTu8rLBjc3eeN9cSKwaF8EGMBNDmhzPNFd",
            }
        )
    )
