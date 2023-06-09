import pyteal as pt
import beaker

season_manager_app = beaker.Application("SeasonManager")

@season_manager_app.external(authorize=beaker.Authorize.only_creator())
def bootstrap(
  seed: pt.abi.PaymentTransaction
) -> pt.Expr:
  return pt.Seq(
    pt.Assert(
      seed.get().receiver() == pt.Global.current_application_address(),
      comment="bootstrap payment must be to app address",
    ),
  )