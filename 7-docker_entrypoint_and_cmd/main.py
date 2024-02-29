import requests
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

SEMO_MINIMAL_COST_URL = "https://reports.sem-o.com/documents/PUB_30MinImbalCost_{period}.xml"
SEMO_PERIOD_FORMAT = "%Y%m%d%H%M"

def fetch_semo_xml(period: str):
    """
    Fetch semo data for a period. This won't be tested.

    Args:
    - period (str): The start time of the period to fetch .

    Returns:
     XML as a string or None if there is an error

    """
    semo_url = SEMO_MINIMAL_COST_URL.format(period=period)
    response = requests.get(semo_url)

    if response.status_code != 200:
        raise Exception(f"Semo data unavailable for period: {period}")

    return response.text

def parse_semo_xml(period: str, semo_xml: str):
    """
    Fetch semo data for a period.

    Args:
    - semo_xml (str): The xml to parse.

    Returns:
     A dictionary of attributes from the xml or None if there is an error parsing the xml.

    """
    try:
        xml_root = ET.fromstring(semo_xml)
        imbalance_xml = xml_root.find("PUB_30MinImbalCost")
        xml_as_dict =  {"period": period,
                        "imbalance_volume": float(imbalance_xml.attrib.get('ImbalanceVolume')),
                        "imbalance_price": float(imbalance_xml.attrib.get('ImbalancePrice')),
                        "imbalance_cost": float(imbalance_xml.attrib.get('ImbalanceCost'))}
    except:
        raise Exception(f"Unable to parse Semo xml.")
    
    return xml_as_dict

def main():

    if len(sys.argv)<2:
        current_time = datetime.now()
        new_time = current_time - timedelta(hours=2)
        period = new_time.strftime('%Y%m%d%H') + "00"
    else:
        period = sys.argv[1]
    
    semo_xml = fetch_semo_xml(period=period)
    semo_xml_as_dict = parse_semo_xml(period=period, semo_xml=semo_xml)
    print(semo_xml_as_dict)

if __name__ == "__main__":
    main()