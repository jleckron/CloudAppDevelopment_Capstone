import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")
    else:
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        payload = kwargs['payload']
        response = requests.post(url, json=payload, params=kwargs)
    except:
        print("Network exception occurred")
    else:
        status_code = response.status_code
        print("With status {}".format(status_code))
        json_data = json.loads(response.text)
        return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["dealers"]
        # For each dealer object
        for dealer_doc in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, dealerId=kwargs['dealer_id'])
    if json_result:
        reviews = json_result["reviews"]
        for review_doc in reviews["docs"]:
            review_obj = DealerReview(
                dealership=review_doc['dealership'],
                name=review_doc['name'],
                purchase=review_doc['purchase'],
                review=review_doc['review'],
                purchase_date=review_doc['purchase_date'],
                car_make=review_doc['car_make'],
                car_model=review_doc['car_model'],
                car_year=review_doc['car_year'],
                sentiment=analyze_review_sentiments(review_doc['review']),
                id=review_doc['id']
            )
            results.append(review_obj)
    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/647cf885-fb7e-4e7e-be3f-050d93bd4793/v1/analyze?version=2022-04-07"
    key = 'tgdV9rAPK3YiNA7YHkKuPJJ3WqZZ6Zo2aJwDNWFvi0qV'
    params = dict()
    params["text"] = dealerreview
    params["version"] = '2020-04-07'
    params["features"] = {"sentiment": {}}

    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'}, 
                        auth=HTTPBasicAuth('apikey', key))
    result = json.loads(response.text)
    if result.get('error'):
        return 'n/a'
    else:
        return result.get('sentiment').get('document').get('label')



