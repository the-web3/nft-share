import smartpy as sp

tstorage = sp.TRecord(result = sp.TOption(sp.TRecord(token_id = sp.TNat, token_info = sp.TMap(sp.TString, sp.TBytes)).layout(("token_id", "token_info")))).layout("result")
tparameter = sp.TVariant(compute = sp.TRecord(data = sp.TRecord(administrator = sp.TAddress, balances = sp.TBigMap(sp.TAddress, sp.TRecord(approvals = sp.TMap(sp.TAddress, sp.TNat), balance = sp.TNat).layout(("approvals", "balance"))), metadata = sp.TBigMap(sp.TString, sp.TBytes), paused = sp.TBool, token_metadata = sp.TBigMap(sp.TNat, sp.TRecord(token_id = sp.TNat, token_info = sp.TMap(sp.TString, sp.TBytes)).layout(("token_id", "token_info"))), totalSupply = sp.TNat).layout((("administrator", ("balances", "metadata")), ("paused", ("token_metadata", "totalSupply")))), params = sp.TNat).layout(("data", "params"))).layout("compute")
tprivates = { }
tviews = { }
