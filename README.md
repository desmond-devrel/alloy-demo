```markdown
# Alloy Integration: Google Sheets + Slack

This Python application demonstrates how to use the Alloy Connectivity API to read from and write to Google Sheets, then post data to Slack. It showcases a complete workflow: adding a new row to a spreadsheet, reading all rows, and sending them to a Slack channel.

## Prerequisites

### 1. Python Installation
- Python 3.7 or higher
- Verify installation: `python --version`

### 2. Required Python Packages
Install dependencies using pip:
```bash
pip install requests python-dotenv
```

Or install from a requirements file:
```bash
pip install -r requirements.txt
```

(If creating a requirements file, include):
```
requests>=2.28.0
python-dotenv>=0.20.0
```

### 3. Alloy Account & API Key
- Sign up for an Alloy account at https://runalloy.com
- Navigate to your dashboard and generate an API key
- Store this key securely (you'll add it to `.env` later)

### 4. Google Sheets Setup
- Create a new Google Sheet or use an existing one
- Note your **Google Sheet ID** (found in the URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`)
- Set up column headers in the first row (e.g., "Name" in A1, "Email" in B1)
- Data will be read/written starting from row 2

### 5. Google Sheets Connection in Alloy
- In your Alloy dashboard, create a new "Google Sheets" connector
- Authorize Alloy to access your Google account
- Copy the **Connection ID** from the connector details
- This ID links your application to your specific Google Sheet

### 6. Slack Webhook Setup
- Go to your Slack workspace's app settings
- Create an Incoming Webhook or use an existing one
- Copy the **Webhook URL** (format: `https://hooks.slack.com/services/...`)
- The webhook URL grants permission to post messages to a specific channel

## Configuration

### Step 1: Create a `.env` File
In the same directory as your Python script, create a `.env` file with the following variables:

```
ALLOY_API_KEY=your_alloy_api_key_here
GOOGLE_SHEET_CONNECTION_ID=your_connection_id_here
GOOGLE_SHEET_ID=your_sheet_id_here
GOOGLE_SHEET_RANGE=Sheet1!A2:B50
SLACK_WEBHOOK_URL=your_slack_webhook_url_here
```

**Environment Variable Details:**
- `ALLOY_API_KEY`: Your Alloy API authentication key
- `GOOGLE_SHEET_CONNECTION_ID`: Connection ID from your Alloy Google Sheets connector
- `GOOGLE_SHEET_ID`: The ID of your target Google Sheet
- `GOOGLE_SHEET_RANGE`: The range of cells to read/write (default: `Sheet1!A2:B50`). Adjust sheet name and range as needed
- `SLACK_WEBHOOK_URL`: Your Slack Incoming Webhook URL

### Step 2: Verify `.env` File Location
Ensure your `.env` file is in the same directory as your Python script. The `load_dotenv()` function will read it automatically.

## Running the Script

### Basic Execution
```bash
python script_name.py
```

Replace `script_name.py` with the actual filename of your Python script.

### What the Script Does
1. **Appends a demo row** to your Google Sheet (adds "Demo Name" and "demo@example.com")
2. **Reads all rows** from the specified range (rows 2-50 by default)
3. **Posts the data to Slack** in a formatted message

### Expected Output
```
Added new row: {'updates': {'updatedCells': 1, ...}}
Read 5 rows from sheet.
Posted 5 rows to Slack!
```

## Function Reference

### `alloy_connectivity_call(connection_id, method, path, body=None, params=None)`
Makes authenticated requests through the Alloy Connectivity API to interact with connected services.

**Parameters:**
- `connection_id`: The Alloy connection ID for the target service
- `method`: HTTP method (`"get"` or `"post"`)
- `path`: API endpoint path (e.g., `/v4/spreadsheets/{id}/values/...`)
- `body`: Request body (optional, for POST requests)
- `params`: Query parameters (optional)

**Returns:** JSON response from the API

### `read_sheet()`
Reads all rows from the Google Sheet within the specified range.

**Returns:** List of rows (each row is a list of cell values)

### `append_row(new_row)`
Appends a single row to the Google Sheet.

**Parameters:**
- `new_row`: List of values to append (e.g., `["Name", "email@example.com"]`)

**Returns:** API response object

### `post_to_slack(rows)`
Sends rows to Slack as a formatted message.

**Parameters:**
- `rows`: List of rows to post

**Returns:** None (prints status to console)

## Customization

### Change the Data Range
Modify the `GOOGLE_SHEET_RANGE` in your `.env` file:
```
GOOGLE_SHEET_RANGE=Sheet2!A1:D100
```

### Modify the Demo Row
Edit the `new_row` variable in the `if __name__ == "__main__"` block:
```python
new_row = ["John Doe", "john@example.com"]
```

### Format Slack Messages
Customize the message format in the `post_to_slack()` function's text generation line.

## Troubleshooting

### "Module not found" error
Ensure all dependencies are installed:
```bash
pip install requests python-dotenv
```

### "Invalid API key" or 401 error
- Verify your `ALLOY_API_KEY` is correct
- Check that your key hasn't expired in the Alloy dashboard
- Ensure the key is properly set in your `.env` file

### "Connection not found" error
- Confirm your `GOOGLE_SHEET_CONNECTION_ID` is correct
- Verify the connection exists in your Alloy dashboard
- Ensure the connection has active authorization to Google Sheets

### "Spreadsheet not found" error
- Double-check your `GOOGLE_SHEET_ID`
- Verify the sheet exists and you have access to it
- Ensure the Alloy-connected Google account has proper permissions

### No message in Slack
- Verify your `SLACK_WEBHOOK_URL` is correct
- Check the webhook URL hasn't expired
- Ensure the webhook is configured for the correct Slack channel

## Security Best Practices

- **Never commit `.env` files to version control.** Add `.env` to your `.gitignore`
- **Keep API keys private.** Don't share your `.env` file or API keys
- **Use environment variables** instead of hardcoding credentials
- **Rotate API keys regularly** for enhanced security
- **Restrict webhook permissions** to only the necessary Slack channels

## Next Steps

- Extend the script to filter or transform data before posting to Slack
- Add error handling and retry logic for production use
- Schedule the script to run periodically using cron jobs (Linux/Mac) or Task Scheduler (Windows)
- Integrate additional connectors supported by Alloy (CRM, database, etc.)

## Support

For issues related to:
- **Alloy API**: Visit https://runalloy.com/docs
- **Google Sheets API**: See https://developers.google.com/sheets/api
- **Slack Webhooks**: Check https://api.slack.com/messaging/webhooks
```

Here's the complete README in plain markdown format you can copy directly!
