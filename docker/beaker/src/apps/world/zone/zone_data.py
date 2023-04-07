from pyteal import (
  abi
)
from typing import Literal


class ZoneData(abi.NamedTuple):
  id: abi.Field[abi.Uint64]
  name: abi.Field[abi.String]
