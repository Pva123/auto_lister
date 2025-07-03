# Auto Lister - Listing Recorder

A simple tool to help you record the steps for posting items on Facebook Marketplace, Kijiji, and eBay.

This tool doesn't post for you automatically. Instead, it logs you in, saves your browser session, and gives you a command to record your own posting steps using Playwright Codegen. This allows you to create robust automation scripts tailored to your exact workflow.

## Setup

1.  **Create and activate a virtual environment (recommended):**

    ```bash
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    venv\Scripts\activate
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Playwright browsers:**
    This downloads the web browsers that Playwright uses for automation.

    ```bash
    playwright install
    ```

## How to Use

1.  **Run the recording helper:**

    ```bash
    python lister.py
    ```

2.  **Select Platforms:** The script will ask you which platforms (Facebook, Kijiji, eBay) you want to log into.

3.  **Log In:** A browser window will open with the login pages for the sites you selected. Log into each one.

4.  **Confirm Login:** Once you've logged in to all platforms, go back to your terminal and press `Enter`.

5.  **Get Codegen Command:** The script will save your login session (cookies) and display a `playwright codegen` command in the terminal.

6.  **Start Recording:**

    - Open a **new terminal** (leave the current one running).
    - Make sure your virtual environment is activated in the new terminal.
    - Copy and paste the `playwright codegen` command into the new terminal and run it.

7.  **Record Your Actions:** A new browser window will open, with you already logged in. Perform all the steps to list one item (e.g., click "Create new listing", fill out the form, upload photos, etc.).

8.  **Generate Code:** When you're finished, close the browser window that Codegen opened. The recorded steps will be saved as Python code inside `lister.py`.

9.  **Use the Recorded Code:** You can now copy the generated code from `lister.py` and use it to build your final, fully automated listing script.

## Files

- `lister.py`: The main script that helps you log in and start a recording session. The code you generate with Codegen will also be saved here.
- `requirements.txt`: Project dependencies.
- `browser_data/`: Stores your saved login sessions. It is created automatically.
- `items/`: You can use this folder to store your item information and images, which your final script can read from.
