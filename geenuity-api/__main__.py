import uvicorn
import requests, os
from dotenv import load_dotenv

def check_server(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        print(f"Server is up and running at {url}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Server is down or not reachable at {url}. Error: {e}")
        return False

if __name__ == "__main__":
    load_dotenv()
    port = os.environ["PORT"]
    check_server(os.environ["SKYVERN_API_URL"])
    reload=True
    uvicorn.run(
        "skyvern-api:skyvern_app",
        host="0.0.0.0",
        port=int(port),
        log_level="info",
        reload=reload,
    )