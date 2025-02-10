import phonenumbers
import pycountry
from phonenumbers import carrier, timezone

def get_phone_number_details(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        country_code = parsed_number.country_code
        region_code = phonenumbers.region_code_for_country_code(country_code)
        country = pycountry.countries.get(alpha_2=region_code)
        
        national_number = parsed_number.national_number
        carrier_name = carrier.name_for_number(parsed_number, 'en')
        time_zones = timezone.time_zones_for_number(parsed_number)
        
        return {
            "country_code": country.alpha_2 if country else None,
            "national_number": national_number,
            "carrier": carrier_name,
            "time_zones": time_zones
        }
    except Exception as e:
        print("Error:", e)
        return None
