import pyteal as pt
import beaker

season_manager_app = beaker.Application("SeasonManager")

@season_manager_app.external(authorize=beaker.Authorize.only_creator())
def bootstrap(
  self,
  seed: pt.abi.PaymentTransaction
):
  return pt.Seq(
    pt.Assert(
      seed.get().receiver() == self.address,
      comment="bootstrap payment must be to app address",
    ),
  )