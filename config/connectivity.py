import socket
import ssl
import urllib.request


def test_connectivity():
    print("---- CONNECTIVITY TESTS ----")

    # Get local IP address from database connection
    # try:
    # from sqlalchemy import create_engine  # New import
    # from database.connection_details import get_database_url  # New import
    #     local_ip_db = "UNKNOWN"
    #     db_url = get_database_url()
    #     engine = create_engine(db_url)
    #     with engine.connect() as connection:
    #         # Get the raw connection object
    #         raw_connection = connection.connection
    #         # For psycopg2, the local address is available via `pgconn.info.local_addr`
    #         # or by inspecting the socket
    #         if hasattr(raw_connection, "info") and hasattr(raw_connection.info, "local_addr"):
    #             local_ip_db = raw_connection.info.local_addr
    #         else:
    #             # Fallback for other drivers or if info.local_addr is not available
    #             # This might not always work depending on the driver
    #             s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #             s.connect(("8.8.8.8", 80))  # Connect to a public DNS server to get local IP
    #             local_ip_db = s.getsockname()[0]
    #             s.close()
    #     print("Local IP (from DB connection):", local_ip_db)
    #     engine.dispose()
    # except Exception as e:
    #     print("Local IP (from DB connection) FAIL:", e)

    # DNS test for oauth2.googleapis.com
    try:
        ip_oauth = socket.gethostbyname("oauth2.googleapis.com")
        print("DNS (oauth2.googleapis.com):", ip_oauth)
    except Exception as e:
        print("DNS (oauth2.googleapis.com) FAIL:", e)
        ip_oauth = None

    # TCP test for oauth2.googleapis.com
    if ip_oauth:
        try:
            s = socket.create_connection((ip_oauth, 443), timeout=5)
            print("TCP (oauth2.googleapis.com): CONNECTED")
            s.close()
        except Exception as e:
            print("TCP (oauth2.googleapis.com) FAIL:", e)

    # HTTPS test for oauth2.googleapis.com
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen("https://oauth2.googleapis.com", timeout=5, context=ctx) as r:
            print("HTTPS (oauth2.googleapis.com) OK:", r.status)
    except Exception as e:
        print("HTTPS (oauth2.googleapis.com) FAIL:", e)

    # DNS test for google.com
    try:
        ip_google = socket.gethostbyname("google.com")
        print("DNS (google.com):", ip_google)
    except Exception as e:
        print("DNS (google.com) FAIL:", e)
        ip_google = None

    # TCP test for google.com
    if ip_google:
        try:
            s = socket.create_connection((ip_google, 443), timeout=5)
            print("TCP (google.com): CONNECTED")
            s.close()
        except Exception as e:
            print("TCP (google.com) FAIL:", e)

    # Raw TCP test to a public IP (e.g., Cloudflare DNS)
    try:
        s = socket.create_connection(("1.1.1.1", 443), timeout=5)
        print("Raw TCP (1.1.1.1:443): CONNECTED")
        s.close()
    except Exception as e:
        print("Raw TCP (1.1.1.1:443) FAIL:", e)

    # HTTPS test for google.com
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen("https://google.com", timeout=5, context=ctx) as r:
            print("HTTPS (google.com) OK:", r.status)
    except Exception as e:
        print("HTTPS (google.com) FAIL:", e)
