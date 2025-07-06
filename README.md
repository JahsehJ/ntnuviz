# ntnuviz

ntnuviz turns raw course data into a readable timetable.

## Run Locally

The project includes:

- an independent python script that exports the timetable as `.xlsx`
- a [`streamlit`](https://streamlit.io) web client.

Dependencies: `pandas`, `openpyxl`, `xlrd` (+ `streamlit` for the web client.)

### Independent Python Script

Run `python3 ntnuviz.py <year(年級)>`. It defaults to take `export.xls` in your working directory and then convert it into `課表.xlsx`.

### Web Client

Run `streamlit run st_client.py` and it will serve a local HTTP server.
