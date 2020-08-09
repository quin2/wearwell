# Wearwell API

## Project
This is the API that the Wearwell Chrome extension uses to calculate sustainability scores for online fashion retail. Relies on pregenerated data on transparency in the industry as well as carbon emissions and energy use for different textile materials.

## Mini-docs
No key needed :)
* brand transparency index: `/v1/brand`
```
POST
{
	"url": "https://example.com"
}

Typical Response:
{
    "brand": "Columbia Sportswear",
    "score": 70.5
}
```
* all data: `/v1/brand`
```
POST
{
	"url": "https://example.com",
	"Materials": ["Wool", "Cotton"]
}

Typical Response:
{
    "brand": "Columbia Sportswear",
    "brandScore": 70.5,
    "material": [
        {
            "formula": 27.98,
            "material": "polyester"
        },
        {
            "formula": 44.95,
            "material": "hemp"
        }
    ]
}
```

## Getting the material array
You might be wondering how to get the list of materials the product is made of! Because we're not doing any scaping on our end (too many ecomm sites have anti-scraping measures and aren't static to boot), you'll have to run a little JavaScript stub on your side, if you want to build an extension with this. That stub is as follows:
```
const result = ["cotton","polyester","hemp","organic cotton","wool","nylon"].filter(m=>document.documentElement.innerText.indexOf(m)>-1)
```

## Deploying
* Procfile and `requirements.txt` designed for Heroku
* set enviroment variables WHOISXMLAPI and WHOISXMLAPI2 to API tokens from [this service](https://whois.whoisxmlapi.com/). We switch between the two because of the low limit of 500 requests per free account

