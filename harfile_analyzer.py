import json
from urllib.parse import urlparse
import tldextract

def extract_domains_from_har(har_path):
    """Extracts and returns a set of domains from the HAR file."""
    domains = {}
    
    with open(har_path, 'r') as file:
        har_data = json.load(file)

    # Navigate through the HAR file structure to find the request URLs
    entries = har_data['log']['entries']
    
    for entry in entries:
        all_cookie_names = set()
        query_names = set()

        url = entry['request']['url']
        cookie_lists = entry['request']['cookies']
        quiery_lists = entry['request']['queryString']

        # process queries
        for queries in quiery_lists:
            if queries:
                if len(queries['value']) > 8:
                    query_names.add((queries['name'],queries['value']))
        print(query_names)

        # process cookies
        for cookies in cookie_lists:
            if cookies:  # Check that the list is not empty
                all_cookie_names.add((cookies['name'], cookies['value']))

        print(all_cookie_names)
        parsed_url = urlparse(url)
        extracted_domain = tldextract.extract(parsed_url.netloc)
        params = parsed_url.params
        queries = parsed_url.query
        

        if extracted_domain.registered_domain not in domains:
            domains[extracted_domain.registered_domain] = {'freq':0, 'queries': set(), 'cookies': set()}

        domains[extracted_domain.registered_domain]['freq'] += 1
        domains[extracted_domain.registered_domain]['queries'].update(query_names)
        domains[extracted_domain.registered_domain]['cookies'].update(all_cookie_names)
    
    return domains

# Replace 'path_to_har_file.har' with the path to your HAR file
har_file_path = '/home/pooneh/ecs289/harfiles/brave/pounehnb.com.har'
found_domains = extract_domains_from_har(har_file_path)
# print("Extracted Domains:", found_domains)

total_requests = 0
for domain, meta in found_domains.items():
    print(domain, found_domains[domain]['freq'])
    # found_domains[domain]['params'] = list(found_domains[domain]['params'])
    found_domains[domain]['queries'] = list(found_domains[domain]['queries'])
    found_domains[domain]['cookies'] = list(found_domains[domain]['cookies'])
    total_requests += found_domains[domain]['freq']
    
print("Total requests: ", total_requests)

with open('/home/pooneh/ecs289/post_processed/brave/pounehnb.com.json', 'w') as f:
    json.dump(found_domains, f, indent=4)
