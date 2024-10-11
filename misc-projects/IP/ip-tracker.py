import requests

def get_public_ip():
    try:
        # Use an external service to get your public IP
        response = requests.get("https://api.ipify.org?format=json")
        response.raise_for_status()
        
        # Extract the IP from the response
        ip_data = response.json()
        ip_address = ip_data.get("ip", "N/A")

        return ip_address
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching public IP: {e}")

def get_ip_data(ip: str):
    try:
        # Use ipinfo.io API to get IP details
        response = requests.get(f"https://ipinfo.io/{ip}/json")

        # Raise an exception if the response has errors
        response.raise_for_status()

        # Parse the JSON response
        ip_data = response.json()

        # Extracting useful data
        ip_address = ip_data.get("ip", "N/A")
        hostname = ip_data.get("hostname", "N/A")
        city = ip_data.get("city", "N/A")
        region = ip_data.get("region", "N/A")
        country = ip_data.get("country", "N/A")
        location = ip_data.get("loc", "N/A")
        org = ip_data.get("org", "N/A")
        postal = ip_data.get("postal", "N/A")
        timezone = ip_data.get("timezone", "N/A")

        # Print the data
        print(f"IP Address: {ip_address}")
        print(f"Hostname: {hostname}")
        print(f"City: {city}")
        print(f"Region: {region}")
        print(f"Country: {country}")
        print(f"Location (lat, long): {location}")
        print(f"Organization: {org}")
        print(f"Postal Code: {postal}")
        print(f"Timezone: {timezone}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching IP data: {e}")

# Example usage
get_ip_data(get_public_ip())
