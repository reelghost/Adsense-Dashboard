# AdSense Analytics Dashboard

## Overview

This Streamlit app provides a user-friendly interface to visualize AdSense
analytics data. Users can view AdSense data for the current date and analyze
page views, clicks, cost per click (CPC) based on country.

## Features

- **Current Date Data**: Displays AdSense data for the current date by default.
- **Analytics by Country**: Visualizes AdSense data based on the countries from
  which the traffic originates.
- **Secure Secrets Management**: Safely stores client secrets and sensitive
  information in the `.toml` file using Streamlit's secrets management system.

### Prerequisites

- Ensure you have Python installed on your system.
- Prior knowledge on [Google AdSense Management API](https://developers.google.com/adsense/management/)

### Installation

1. Navigate to the project directory in your terminal.
2. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```

### Configuration
- Use the `decode.py` to decode your secrets file and paste the string in the `secrets.toml` file
- Ensure that the `secrets.toml` file is placed in the `.streamlit` directory if
  you are running it locally
- Read


### Running the App

1. After installing the dependencies, run the Streamlit app with the following
   command:
   ```
   streamlit run adsense.py
   ```
2. The app will open in your default web browser, allowing you to interact with
   the AdSense Analytics Dashboard.



## Contributing

Contributions are welcome! If you have any suggestions, feature requests, or bug
reports, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- Built with [Streamlit](https://streamlit.io/)
- AdSense data retrieved using the
  [Google AdSense Management API](https://developers.google.com/adsense/management/)
