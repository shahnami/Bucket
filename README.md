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

## Collections

Currently, the following collections have been created:

- AuthCollection
- AWSCollection
- BrochureCollection
- ClientCollection
- DNSCollection
- EnvironmentCollection
- InputCollection
- NoneCollection
- OWACollection
- PaymentCollection
- ProductionCollection
- SocialCollection
- StagingCollection
- VPNCollection

Feel free to modify any collection code, or add your own collections.

When creating a new collection, use the following template code:

```python
from .collection import Collection

class NewCollection(Collection):
    """ New Collection class

        Describe what your collection does in as much detail as you can here.
    """

    def __init__(self):
        Collection.__init__(self)
        self.name = 'New Collection'
        self.check = {'domain': True, 'content': True, 'status': True}
        self.keywords = ['enter keywords here for which you want to scrape']
        self.set_weight()
```

Each Collection is abstracted from the `Collection` class.

- `self.keywords` defines _what_ the scraper should be looking for.
- `self.check` defines _where_ it should be looking.

Optionally, you can overwrite the `validate` method for more complex matching.

```python
from .collection import Collection
from ..page import Page

class NewCollection(Collection):
    ...
    def validate(self, *, page: Page):
        """ Write your own validation method here based on the keywords. """
```

When executing the scraper with multiple collections, conflicts may arise in terms of priority.
To solve this, modify the `config.py` file and assign priorities to the collections as you see fit.

```python
WEIGHTS: dict = {
    "OWA Collection": 106,
    "VPN Collection": 105,
    "Staging Collection": 104,
    "None Collection": 103,
    "Auth Collection": 102,
    "AWS Collection": 101,
    "Client Collection": 100,
    "DNS Collection": 100,
}
```

The higher the weight, the higher the priority.
Weights should start with a priority of `100` to stay consistent.

## Notes

DNS collection is still experimental, and does not work well with the other collections. DNS collection also uses its own exporter.
If you intend to use the DNS collection, comment out other collections and the csv & json exporters.

- Create your own collection in `./collections/`
- Create your own exporters in `./exporters/`
