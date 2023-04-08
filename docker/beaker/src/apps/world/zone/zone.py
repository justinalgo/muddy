import pyteal as pt
import beaker
from typing import Literal

from .zone_data import ZoneData


class ZoneState:
  def __init__(self):
    self.data = beaker.lib.storage.BoxMapping(pt.abi.StaticBytes[Literal[4]], ZoneData)

app = beaker.Application(
  "Zone",
  state=ZoneState()
)

@app.external(authorize=beaker.Authorize.only_creator())
def bootstrap(
  id: pt.abi.Uint64,
  name: pt.abi.String,
  seed: pt.abi.PaymentTransaction
) -> pt.Expr:
  """initialize contract of this zone and add seed funds"""
  return pt.Seq(
    pt.Assert(
      id.get() > pt.Int(0),
      comment="zone ID must be greater than 0"
    ),
    pt.Assert(
      seed.get().receiver() == pt.Global.current_application_address(),
      comment="bootstrap payment must be to app address",
    ),
    (zd := ZoneData()).set(id, name),
    (box_key := pt.abi.make(pt.abi.StaticBytes[Literal[4]])).set(pt.Bytes("data")),
    app.state.data[box_key].set(zd),
  )