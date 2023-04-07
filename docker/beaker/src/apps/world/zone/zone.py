import pyteal as pt
import beaker

app = beaker.Application("Zone")

@app.external(authorize=beaker.Authorize.only_creator())
def bootstrap(
  seed: pt.abi.PaymentTransaction
) -> pt.Expr:
  """initialize contract of this zone and add seed funds"""
  return pt.Seq(
    pt.Assert(
      seed.get().receiver() == pt.Global.current_application_address(),
      comment="bootstrap payment must be to app address",
    ),
  )