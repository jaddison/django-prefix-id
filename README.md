### Overview

`django-prefix-id` is a simple package that contains a single Django model 
field, `PrefixIDField`. `PrefixIDField` is
- based on Django's `CharField`
- allows using a prefix (recommended for context)
  - enables some very interesting product usage and querying patterns 
- autogenerates a unique id by default (auto-including the prefix, if provided)
  - uses `uuid.uuid4()` to generate a 128-bit integer, which is then 
    base62-encoded 
- auto-sets the `max_length` field property, factoring in the provided prefix length 
  and a known max length of 22 characters for a base62-encoded 128-bit integer

**Why work with IDs like `7584358` or `'7fca5f1d-f867-4696-960b-e57274cc5647'` 
when you could have something swanky like `'user_4wr7jBDTEqVBCsXEih4zfP'`?**

If you already like to use UUIDs as IDs, you should use `django-prefix-id`! If you currently use
autoincrementing IDs, you should also consider using `django-prefix-id`, from an obfuscation 
point of view.

### Installation

```shell
$ pip install django-prefix-id
```

### Usage
```python
from prefix_id import PrefixIDField

class Book(models.Model):
    id = PrefixIDField(prefix="book", primary_key=True)
    title = models.CharField(max_length=100, blank=False)
    ...
```

Make your migrations, as you normally would:
```shell
$ python manage.py makemigrations
```

### Development

```shell
$ pip -m venv venv
$ source /venv/bin/activate
$ pip install -r requirements.txt
```

### Testing

Manually run tests:
```shell
$ pytest
```

Test coverage is at 100%. To get test coverage output:
```shell
$ pytest --cov --cov-report html
# OR
$ pytest --cov
```

To cover a breadth of likely usage scenarios, `tox` is the tool of 
choice. It is set up with a matrix covering various combinations of 
Python versions 3.8 - 3.12 with Django 4.2 and 5.0.

See `tox.ini` to enable testing Django versions as far back as Django 
3.2 - tests pass across the board, but for simplicity only latest LTS 
Django and other currently supported versions will be considered in 
scope.

Run the test suite against all enabled versions:

```shell
$ tox
```

### Backstory and Inspiration

Stripe-like prefixed entity IDs have long been a topic of interest to me, 
and the improved user experience that they can provide. I'd gone through 
a couple of iterations with FastAPI and Django - and thought I might as 
well release something that I'm happy with sharing publicly.

About 80% through this effort, I found yunojuno's 
[django-charid-field](https://github.com/yunojuno/django-charid-field/) 
project, and took some further inspiration from it - so thanks to them! 

(It also appears we have other project interests in common!)