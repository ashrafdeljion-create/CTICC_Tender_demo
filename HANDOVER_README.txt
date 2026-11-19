CTICC Dashboard Tender Demonstration Handover
================================================

Live demo
---------
https://visible-alone-seekers-homes.trycloudflare.com

Access:
- No login is required.
- Open the link using an internet-connected browser.
- The first page load may take a few seconds.
- This is a temporary public HTTPS tunnel to the dashboard running on this
  workstation. The URL is valid only while the tunnel and local dashboard remain
  active.

Demo highlights
---------------
- Executive dashboard and KPI cards
- Monthly and quarterly comparison charts
- Benchmark configuration
- Under-benchmark event alerts
- Event-name and event-ID search
- Individual event interview reports
- Excel report downloads
- Management evidence and corrective-action notes
- Historical data migration plan
- Training options
- User guide

Data notice
-----------
All event names and results are anonymised dummy data. No confidential CTICC
data is included.

Files
-----
- app.py: Streamlit dashboard application
- .streamlit/config.toml: CTICC demonstration theme
- test_app.py: focused application tests
- requirements.txt: Python dependencies
- PM_EMAIL_DRAFT.txt: email prepared for the project team
- screenshots/: screenshots covering the requested tender demonstration areas

Local startup
-------------
From the project folder:

.venv\Scripts\python.exe -m streamlit run app.py --server.headless=true

The local URL is http://127.0.0.1:8501.

Test status
-----------
The focused Streamlit test suite passed: 2 tests.
