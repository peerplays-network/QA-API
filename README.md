# QA-API
This API is for QA testing purposes and is meant to act as a wrapper to the Market Maker API. To the user, this will simply look like a superset of the Market Maker API.

Edit config.yaml with the URL to your bookieapi instance

To run, ensure the bookieapi from the MarketMaker project is running, and run with:
python3 qaapi.py
https://github.com/PBSA/MarketMaker

DOCKER
To run a dockerized container, first edit the Dockerfile with you pertinent connection information, then run
docker build -t pbsa/qa-api:1.0 . 
docker-compose up -d


Documentation is stored in docs/build/html/qaapi.html
