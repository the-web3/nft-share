import smartpy as sp

class Contract(sp.Contract):
  def __init__(self):
    self.init_type(sp.TRecord(result = sp.TOption(sp.TRecord(token_id = sp.TNat, token_info = sp.TMap(sp.TString, sp.TBytes)).layout(("token_id", "token_info")))).layout("result"))
    self.init(result = sp.none)

  @sp.entry_point
  def compute(self, params):
    sp.set_type(params.params, sp.TNat)
    __s5 = sp.local("__s5", params.data.token_metadata[params.params])
    self.data.result = sp.some(__s5.value)

sp.add_compilation_target("test", Contract())