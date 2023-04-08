import pyteal as pt
import beaker
import algosdk
from algosdk.encoding import encode_address
from algosdk.atomic_transaction_composer import TransactionWithSigner
from algosdk.transaction import (
  PaymentTxn
)

from apps import Zone, zone_bootstrap
from apps.world.zone import ZoneData

ALGOD_ADDRESS = "http://host.docker.internal:4001"
KMD_ADDRESS = "http://host.docker.internal:4002"
INDEXER_ADDRESS = "http://host.docker.internal:8980"


record_codec = algosdk.abi.ABIType.from_string(str(ZoneData().type_spec()))
def print_boxes(app_client: beaker.client.ApplicationClient) -> None:
  boxes = app_client.get_box_names()
  print(f"{len(boxes)} boxes found")
  for box_name in boxes:
    contents = app_client.get_box_contents(box_name)
    zone_data = record_codec.decode(contents)
    print(f"{box_name} => {zone_data}")

def demo() -> None:
  zones = 0

  creator = beaker.sandbox.get_accounts(kmd_address=KMD_ADDRESS).pop()
  app_client = beaker.client.ApplicationClient(
    client=beaker.sandbox.get_algod_client(address=ALGOD_ADDRESS),
    app=Zone,
    signer=creator.signer,
  )

  # Deploy the app on-chain
  app_id, app_addr, txid = app_client.create()
  print(f"""Deployed app in txid {txid}\rApp ID: {app_id}\rAddress: {app_addr}""")

  sp = app_client.get_suggested_params()
  sp.flat_fee = True
  sp.fee = 1000
  ptxn = PaymentTxn(
      sender=creator.address, 
      sp=sp, 
      receiver=app_client.app_addr, 
      amt=1000000000
  )

  print(f"Bootstrapping app {app_id}")
  # Call the `bootstrap` method
  app_client.call(
    method=zone_bootstrap,
    seed=TransactionWithSigner(
      txn=ptxn, 
      signer=creator.signer
    ),
    id=zones + 1,
    name="The First Zone",
    boxes=[[app_client.app_id, "data"]]
  )
  print_boxes(app_client)

if __name__ == "__main__":
  demo()