# Lokimo backend coding test

This project is a backend RESTful API service for a technical coding test at Lokimo.

## Project Description

The project is backend application that uses [Django REST Framework](https://www.django-rest-framework.org/), [PostgreSQL](https://www.postgresql.org/) and [GeoDjango](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/) to serve APIs.

The APIs serve data about real estate lisintgs located in Loire-Atlantique departement on the west coast of France.

To simulate and test the project, data samples were provided in a JSON file named "lokimo-dataset-bakend-test.json".

## Data

The samples JSON file contains 250 of real estate advertisements. Some listings' data were missing or null while others were completly provided on the 255 examples.

advertisement data can be mandatory, optional (not given in some cases) or null/blank. The choice of making some fields mandatory and others optional was made on the provided data samples where I noticed some values were always provided and others sometimes are not and may be null or blank.

The database schema follows the same structure of the provided json file. It consists of 4 tables (Advertisement, Data, Status and Position).

The main table is called "Advertisement". Each advertisment is a listing of a house or an appartement to sell or to rent.

The advertisement table contains some fields like price, rooms, surface, etc. and has two other tables called "Data" and "Position".

The "Data" table contains details of the listing including the table "Status"

The "Status" table gives details about the status of the listing.

The "Position" table has the location of the property in terms of longitude and latitude coordinates. This table use GeoDjango Point data field.

## APIs

The project API services are :

- get all the existing advertisements or post a new one to the database

```bash
  http://localhost:8000/ads/
```

- get or delete an advertisement using primary key (id)

```bash
  http://localhost:8000/ads/{id}
```

- get all the advertisement with a given city code.

```bash
  http://localhost:8000/ads/city/{city-code}
```

- get the average meter square price of advertisements within a distance from a given location.

```bash
  http://localhost:8000/ads/geoprice/{latitude}/{longitude}/{radius}
```

- get a price estimation of a house or an appartement given its surface, number of rooms and location.

```bash
  http://localhost:8000/ads/estimateprice/{house-type}/{rooms}/{surface}/{latitude}/{longitude}
```

## Getting started

- To run the project you must have [docker](https://www.docker.com/) installed

- First clone the project then open a terminal in the folder project

```bash
git clone https://github.com/y05f/lokimo_backend.git
cd lokimo_backend
```

- Start docker then build the images and run the containers:

```bash
docker-compose up -d --build
```

- Open [http://localhost:8000](http://localhost:8000) and you will see the django rest framework API documentations using swagger-ui.

## Initialize data

To initialize data with the given samples from JSON file type :

```bash
docker-compose exec web  python manage.py resetdata --delete
```

This will delete all existing data and insert raw data from the json file "lokimo-dataset-bakend-test.json" to project's database.

You can omit the parameter --delete if you want to insert raw data wihout deleting the existing one.

The script behind this command is located in the management folder in advertisement folder.

## Runing tests

- To run tests just type :

```bash
docker-compose exec web  python manage.py test
```

- The testing phasse consists of 7 tests of all the endpoints where the file "test_data.json" is used as testing database.

## How to read and explore the project

- The project folder contains 3 main folders (advertisement, api, backend).
- The backend folder is the main django folder project
- The advertisement folder is a django app which contains the advertisement models and script to reset data using "lokimo-dataset-bakend-test.json"
- The api folder contains the serilizers, the views and urls plus the test units.
- The following tree folder shows only the files that I have edited or created excluding the other untouched or default files and folders:

```bash
├── Dockerfile
├── advertisement
│   ├── admin.py # where models are registered to be accessed by admin
│   ├── management
│   │   └── commands
│   │   └── resetdata.py # contains a script to delete and insert data from "lokimo-dataset-bakend-test.json"
│   ├── models.py # where the models are defined and created (Advertisement, Data, Status and Position)
├── api
│   ├── serializers.py # contains serilizers for the 4 models
│   ├── test
│   │   ├── test_estimate_price.py # a test unit for estimate price endpoint
│   │   ├── test_get_city_ads.py # a test unit for city code endpoint
│   │   ├── test_get_delete_ads.py # a test unit for get and delete advertisement
│   │   ├── test_get_geo_prices.py # a test unit for square meter price endpoint
│   │   └── test_list_post_ads.py # a test unit for list and post endpoint
│   ├── urls.py # where endpoints are defined
│   └── views.py # where logic and views are defined
├── backend
│   ├── settings.py # django project settings
│   ├── urls.py # django project main urls
├── docker-compose.yml
├── lokimo-dataset-backend-test.json
├── requirements.txt
└── test_data.json
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Credits

- [Django for Professionals Production websites with Python & Django](https://djangoforprofessionals.com/) by William S. Vincent

- [https://docs.djangoproject.com/en/4.1/howto/](https://docs.djangoproject.com/en/4.1/howto/)

- [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)

- [https://docs.djangoproject.com/en/4.1/ref/contrib/gis/](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/)

- [https://drf-spectacular.readthedocs.io/en/latest/readme.html#take-it-for-a-spin](https://drf-spectacular.readthedocs.io/en/latest/readme.html#take-it-for-a-spin)
