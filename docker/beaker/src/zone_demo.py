import pyteal as pt
import beaker

from apps import Zone


def demo() -> None:
  app_client = beaker.client.ApplicationClient(
    client=beaker.sandbox.get_algod_client(),
    app=Zone,
    signer=beaker.sandbox.get_accounts().pop().signer,
  )

  # Deploy the app on-chain
  app_id, app_addr, txid = app_client.create()
  print(
    f"""Deployed app in txid {txid}
    App ID: {app_id} 
    Address: {app_addr} 
    """
  )

if __name__ == "__main__":
  demo()