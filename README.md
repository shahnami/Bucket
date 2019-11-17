# bucket

A simple script that parses a bunch of targets (domain names) and categorises them into collections ("buckets") based on the presence of certain keywords.

## Usage

Create a `targets.txt` file and enter the domain names you wish to scrape.

```
example.com
amazon.com
www.netflix.com
```

Modify the `start.py` file and execute the following commands:

```
> pipenv shell --python 3
> pip3 install -r requirements.txt
> pipenv run python start.py
```
