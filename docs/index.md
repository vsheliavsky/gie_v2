# Quickstart Guide

This guide provides a quick start for using the `GieClient` class to interact with the GIE API, enabling you to perform various queries such as retrieving storage data, unavailability information, EIC listings, and news updates.

## **Installation**

```pip install roiti-gie-v2```

## **Basic Usage**

The GieClient class requires an API key to authenticate with the GIE API. You can get one by registering here: https://alsi.gie.eu/#/api and creating a key that's valid for both AGSI and ALSI.

```python
from XXXXX.clients import gie_client
from XXXXX.api_models.platform import APIType
```
Create a client instance:
```client = GieClient(api_key="your_api_key")```

Or create a client instance with a custom session:
```
session = requests.Session()
session.headers["x-key"] = "your_api_key"
client = GieClient(api_key="your_api_key", session=session)
```

You'll also need to import the APIType you inted to query:

```
from XXXXX.api_models.platform import APIType
```

## **Methods Overview**

The GieClient class includes various methods to interact with different parts of the GIE API:

    fetch: Sends a GET request to a specified API endpoint. This serves as a base method and shouldn't be used directly.
    query_storage: Retrieves storage data with filters such as date, type, country, etc.
    query_unavailability: Retrieves data on planned or unplanned unavailability.
    query_eic_listing: Retrieves EIC listing or general API information.
    query_news_listing: Retrieves general news or a specific news item.

**Examples**

Here are some examples to get you started with each method:
Fetch Data from API

##**Query Storage Data**

```
import datetime
response = client.query_storage(
    api_type=APIType.AGSI,
    page=1,
    size=50,
    from_date=datetime.date(2023, 1, 1),
    to_date=datetime.date(2023, 12, 31),
    country="DE"
)
```

##**Query Unavailability Data**

```
response = client.query_unavailability(
    api_type=APIType.AGSI,
    page=1,
    size=50,
    from_date=datetime.date(2023, 1, 1),
    to_date=datetime.date(2023, 12, 31),
    country="DE",
    type="Planned"
)
```

##**Query EIC Listing**

```
response = client.query_eic_listing(api_type=APIType.AGSI, show_listing=True)
```

##**Query News Listing**

```
response = client.query_news_listing(api_type=APIType.AGSI)
```

For detailed parameter information and error handling, refer to the individual client documentation pages.
