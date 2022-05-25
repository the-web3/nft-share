import smartpy as sp

class Contract(sp.Contract):
  def __init__(self):
    self.init_type(sp.TRecord(last = sp.TOption(sp.TAddress)).layout("last"))
    self.init(last = sp.none)

  @sp.entry_point
  def target(self, params):
    self.data.last = sp.some(params)

sp.add_compilation_target("test", Contract())