# Webpage Monitor

This is a simple Python script to monitor the status of a website and send alerts to a Slack channel if the website goes down or comes back up.

## Requirements

- Python 3.6+
- `requests` library
- `python-dotenv` library

## Installation

1. Clone the repository:
   
    ```sh
    git clone https://github.com/ddeveloper72/Webpage-Monitor.git
    cd Webpage-Monitor
    ```
    
2. Create a virtual environment and activate it:
 
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory of the project and add your environment variables:

    ```env
    DEVELOPMENT=True
    URL_DEVELOPMENT=https://your-development-url.com
    URL_PRODUCTION=https://your-production-url.com
    SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/slack/webhook/url

    ```

## Usage

Run the script:

## References

Block Kit by Slack provides a clean and Consistent UI framework for Slack Apps.  See [slack api](https://api.slack.com/block-kit#:~:text=Customize%20the%20order%20and%20appearance%20of%20information%20and,be%20stacked%20and%20arranged%20to%20create%20app%20layouts.)