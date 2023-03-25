from kiteconnect import KiteConnect
import requests

# need to work on this one


def get_session_id(api_key: str):
    url = "https://kite.zerodha.com/connect/login?api_key="+api_key
    r = requests.get(url)
    print(r)


def connect_to_zerodha(api_key: str, api_secret: str):
    try:
        kite = KiteConnect(api_key=api_key)
        # get_session_id(api_key)
        # data = kite.generate_session(
        #    "rWVSn3ukPEw5Y6EGZaHl4HHO2qCJTg2H", api_secret=api_secret)
        # print(data)
        # kite.set_access_token(data["access_token"])
        kite.set_access_token("qYe4QZ5sdVbQH289jijVGEOgvg4ulM2E")
        return kite
    except Exception as e:
        print(f"error connecting zerodha {e}")
