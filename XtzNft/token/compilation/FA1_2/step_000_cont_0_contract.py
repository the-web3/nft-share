import smartpy as sp

class Contract(sp.Contract):
  def __init__(self):
    self.init_type(sp.TRecord(administrator = sp.TAddress, balances = sp.TBigMap(sp.TAddress, sp.TRecord(approvals = sp.TMap(sp.TAddress, sp.TNat), balance = sp.TNat).layout(("approvals", "balance"))), metadata = sp.TBigMap(sp.TString, sp.TBytes), paused = sp.TBool, token_metadata = sp.TBigMap(sp.TNat, sp.TRecord(token_id = sp.TNat, token_info = sp.TMap(sp.TString, sp.TBytes)).layout(("token_id", "token_info"))), totalSupply = sp.TNat).layout((("administrator", ("balances", "metadata")), ("paused", ("token_metadata", "totalSupply")))))
    self.init(administrator = sp.address('tz1iJzB6WsHiSd9TJgmQHNXwc4eyRs9GvfJj'),
              balances = {},
              metadata = {'' : sp.bytes('0x697066733a2f2f516d616941556a3146464e4759547538724c426a633365654e3963534b7761463845474d424e446d687a504e4664')},
              paused = False,
              token_metadata = {0 : sp.record(token_id = 0, token_info = {'decimals' : sp.bytes('0x3138'), 'icon' : sp.bytes('0x68747470733a2f2f736d61727470792e696f2f7374617469632f696d672f6c6f676f2d6f6e6c792e737667'), 'name' : sp.bytes('0x57656e776f546f6b656e'), 'symbol' : sp.bytes('0x575754')})},
              totalSupply = 0)

  @sp.entry_point
  def approve(self, params):
    sp.set_type(params, sp.TRecord(spender = sp.TAddress, value = sp.TNat).layout(("spender", "value")))
    sp.if ~ (self.data.balances.contains(sp.sender)):
      self.data.balances[sp.sender] = sp.record(approvals = {}, balance = 0)
    sp.verify(~ self.data.paused, 'FA1.2_Paused')
    sp.verify((self.data.balances[sp.sender].approvals.get(params.spender, default_value = 0) == 0) | (params.value == 0), 'FA1.2_UnsafeAllowanceChange')
    self.data.balances[sp.sender].approvals[params.spender] = params.value

  @sp.entry_point
  def burn(self, params):
    sp.set_type(params, sp.TRecord(address = sp.TAddress, value = sp.TNat).layout(("address", "value")))
    sp.verify(sp.sender == self.data.administrator, 'FA1.2_NotAdmin')
    sp.verify(self.data.balances[params.address].balance >= params.value, 'FA1.2_InsufficientBalance')
    self.data.balances[params.address].balance = sp.as_nat(self.data.balances[params.address].balance - params.value)
    self.data.totalSupply = sp.as_nat(self.data.totalSupply - params.value)

  @sp.entry_point
  def getAdministrator(self, params):
    sp.set_type(sp.fst(params), sp.TUnit)
    __s6 = sp.local("__s6", self.data.administrator)
    sp.set_type(sp.snd(params), sp.TContract(sp.TAddress))
    sp.transfer(__s6.value, sp.tez(0), sp.snd(params))

  @sp.entry_point
  def getAllowance(self, params):
    __s7 = sp.bind_block("__s7"):
    with __s7:
      sp.if self.data.balances.contains(sp.fst(params).owner):
        sp.result(self.data.balances[sp.fst(params).owner].approvals.get(sp.fst(params).spender, default_value = 0))
      sp.else:
        sp.result(0)
    sp.set_type(sp.snd(params), sp.TContract(sp.TNat))
    sp.transfer(__s7.value, sp.tez(0), sp.snd(params))

  @sp.entry_point
  def getBalance(self, params):
    __s8 = sp.bind_block("__s8"):
    with __s8:
      sp.if self.data.balances.contains(sp.fst(params)):
        sp.result(self.data.balances[sp.fst(params)].balance)
      sp.else:
        sp.result(0)
    sp.set_type(sp.snd(params), sp.TContract(sp.TNat))
    sp.transfer(__s8.value, sp.tez(0), sp.snd(params))

  @sp.entry_point
  def getTotalSupply(self, params):
    sp.set_type(sp.fst(params), sp.TUnit)
    __s9 = sp.local("__s9", self.data.totalSupply)
    sp.set_type(sp.snd(params), sp.TContract(sp.TNat))
    sp.transfer(__s9.value, sp.tez(0), sp.snd(params))

  @sp.entry_point
  def mint(self, params):
    sp.set_type(params, sp.TRecord(address = sp.TAddress, value = sp.TNat).layout(("address", "value")))
    sp.verify(sp.sender == self.data.administrator, 'FA1.2_NotAdmin')
    sp.if ~ (self.data.balances.contains(params.address)):
      self.data.balances[params.address] = sp.record(approvals = {}, balance = 0)
    self.data.balances[params.address].balance += params.value
    self.data.totalSupply += params.value

  @sp.entry_point
  def setAdministrator(self, params):
    sp.set_type(params, sp.TAddress)
    sp.verify(sp.sender == self.data.administrator, 'FA1.2_NotAdmin')
    self.data.administrator = params

  @sp.entry_point
  def setPause(self, params):
    sp.set_type(params, sp.TBool)
    sp.verify(sp.sender == self.data.administrator, 'FA1.2_NotAdmin')
    self.data.paused = params

  @sp.entry_point
  def transfer(self, params):
    sp.set_type(params, sp.TRecord(from_ = sp.TAddress, to_ = sp.TAddress, value = sp.TNat).layout(("from_ as from", ("to_ as to", "value"))))
    sp.verify((sp.sender == self.data.administrator) | ((~ self.data.paused) & ((params.from_ == sp.sender) | (self.data.balances[params.from_].approvals[sp.sender] >= params.value))), 'FA1.2_NotAllowed')
    sp.if ~ (self.data.balances.contains(params.from_)):
      self.data.balances[params.from_] = sp.record(approvals = {}, balance = 0)
    sp.if ~ (self.data.balances.contains(params.to_)):
      self.data.balances[params.to_] = sp.record(approvals = {}, balance = 0)
    sp.verify(self.data.balances[params.from_].balance >= params.value, 'FA1.2_InsufficientBalance')
    self.data.balances[params.from_].balance = sp.as_nat(self.data.balances[params.from_].balance - params.value)
    self.data.balances[params.to_].balance += params.value
    sp.if (params.from_ != sp.sender) & (~ (sp.sender == self.data.administrator)):
      self.data.balances[params.from_].approvals[sp.sender] = sp.as_nat(self.data.balances[params.from_].approvals[sp.sender] - params.value)

  @sp.entry_point
  def update_metadata(self, params):
    sp.verify(sp.sender == self.data.administrator, 'FA1.2_NotAdmin')
    self.data.metadata[params.key] = params.value

sp.add_compilation_target("test", Contract())