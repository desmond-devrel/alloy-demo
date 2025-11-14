import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

ALLOY_API_KEY = os.getenv("ALLOY_API_KEY")
GOOGLE_SHEET_CONNECTION_ID = os.getenv("GOOGLE_SHEET_CONNECTION_ID")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_SHEET_RANGE = os.getenv("GOOGLE_SHEET_RANGE", "Sheet1!A2:B50")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

ALLOY_BASE_URL = "https://connect.runalloy.com/connectors"


def alloy_connectivity_call(connection_id, method, path, body=None, params=None):
    """
    Makes a request to Alloy Connectivity API.
    """
    headers = {
        "Authorization": f"Bearer {ALLOY_API_KEY}",
        "x-api-version": "2025-09",
        "Content-Type": "application/json"
    }

    payload = {
        "connectionId": connection_id,
        "method": method.lower(),
        "path": path
    }
    if body is not None:
        payload["body"] = body
    if params is not None:
        payload["params"] = params

    resp = requests.post(ALLOY_BASE_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def read_sheet():
    """Reads rows from Google Sheet."""
    path = f"/v4/spreadsheets/{GOOGLE_SHEET_ID}/values/{GOOGLE_SHEET_RANGE}"
    response = alloy_connectivity_call(GOOGLE_SHEET_CONNECTION_ID, "get", path)
    return response.get("values", [])


def write_sheet(new_row):
    """Appends a new row to the Google Sheet."""
    path = f"/v4/spreadsheets/{GOOGLE_SHEET_ID}/values/{GOOGLE_SHEET_RANGE}:append"
    body = {
        "values": [new_row],
        "valueInputOption": "RAW"
    }
    response = alloy_connectivity_call(GOOGLE_SHEET_CONNECTION_ID, "post", path, body=body)
    return response


def send_to_slack(rows):
    """Posts rows to Slack."""
    if not rows:
        print("No rows to send to Slack.")
        return
    text = "\n".join([
        f"- {row[0]}" if len(row) == 1 else f"- {row[0]} — {row[1]}"
        for row in rows
    ])
    slack_resp = requests.post(SLACK_WEBHOOK_URL, json={"text": text})
    slack_resp.raise_for_status()
    print(f"Sent {len(rows)} rows to Slack successfully!")


def main():
    try:
        # Optional: write a demo row
        new_row = ["Demo Name", "demo@example.com"]
        write_resp = write_sheet(new_row)
        print("Added new row:", write_resp)

        # Read all rows
        rows = read_sheet()
        print(f"Read {len(rows)} rows from Google Sheet.")

        # Send rows to Slack
        send_to_slack(rows)

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
