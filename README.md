# ntnuviz

ntnuviz turns raw course data into a readable timetable.

## Run Locally

The project includes:

- a standalone Python script that exports the timetable as `.xlsx`
- a [`Streamlit`](https://streamlit.io) web client

Dependencies:

- `pandas`
- `openpyxl`
- `xlrd`
- `Jinja2`
- `streamlit` (for the web client)

### Standalone Python Script

Run `python3 ntnuviz.py <year(年級)>`. It takes `export.xls` in your working directory and then converts it into `課表.xlsx`.

### Web Client

Run `streamlit run st_client.py` to start a local HTTP server.
