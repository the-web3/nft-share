import smartpy as sp

tstorage = sp.TRecord(last = sp.TOption(sp.TAddress)).layout("last")
tparameter = sp.TVariant(target = sp.TAddress).layout("target")
tprivates = { }
tviews = { }
