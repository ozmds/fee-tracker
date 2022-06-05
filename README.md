# fee-tracker

A basic commandline application that accepts a set of fees in CSV format, and then processes them and can be asked questions them. 

To run the application you can run:
```
python main.py raw_fees.csv
```
You can also install the packages in the requirements/base.txt file but they are only required for linting and unit testing

To run all unit tests:
```
pytest --cov=. --cov-report term-missing -s
```
