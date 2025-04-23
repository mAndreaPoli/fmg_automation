import sys, random, time, csv, os
import ipaddress
from pyFMG.fortimgr import FortiManager
from dotenv import load_dotenv

load_dotenv()

FMG_IP = os.getenv('FMG_IP')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
ADOM = os.getenv('ADOM')

def create_firewall_address(fmg, name, subnet_cidr, comment="", color=None):
    net = ipaddress.ip_network(subnet_cidr, strict=False)
    
    data = {
        "name": name,
        "type": "ipmask",
        "subnet": f"{net.network_address}/{net.prefixlen}",
        "comment": comment,
    }
    
    if color is not None and isinstance(color, int) and 1 <= color <= 32:
        data["color"] = color
    else:
        data["color"] = random.randint(1, 32)
    
    url = f"pm/config/adom/{ADOM}/obj/firewall/address"
    
    fmg.debug = True
    response = fmg.set(url, **data)
    fmg.debug = False
    
    return response

def read_csv_addresses(csv_file):
    addresses = []
    
    if not os.path.exists(csv_file):
        print(f"Error: File {csv_file} does not exist.")
        return addresses
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            if 'subnet' not in reader.fieldnames:
                print("Error: CSV file must contain a 'subnet' column.")
                return addresses
            
            for i, row in enumerate(reader, 1):
                if not row['subnet']:
                    print(f"Line {i}: Missing 'subnet' field, line ignored.")
                    continue
                
                address = {
                    'name': row.get('name', f"host_{str(i).zfill(4)}"),
                    'subnet': row['subnet'],
                    'comment': row.get('comment', f"Imported from CSV on {time.strftime('%Y-%m-%d')}"),
                }
                
                if 'color' in row and row['color']:
                    try:
                        address['color'] = int(row['color'])
                    except ValueError:
                        pass
                
                addresses.append(address)
                
    except Exception as e:
        print(f"Error reading CSV: {e}")
        
    return addresses

def create_random_addresses(count=10):
    addresses = []
    
    for i in range(1, count+1):
        host_id = str(i).zfill(4)
        random_host = random.randint(1, 16777214)
        
        address = {
            'name': f"host_{host_id}",
            'subnet': f"10.0.0.0/{random_host}/32",
            'comment': f"Host #{i} created for TEST via pyfmg on {time.strftime('%Y-%m-%d')}",
        }
        
        addresses.append(address)
        
    return addresses

def main():
    csv_file = None
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    
    with FortiManager(FMG_IP, USERNAME, PASSWORD, disable_request_warning=False) as fmg:
        fmg.login()
        
        fmg.lock_adom(ADOM)
        try:
            if csv_file:
                print(f"Reading addresses from {csv_file}...")
                addresses = read_csv_addresses(csv_file)
                if not addresses:
                    print("No valid addresses found in CSV. Using random addresses.")
                    addresses = create_random_addresses()
            else:
                print("No CSV file specified. Generating random addresses...")
                addresses = create_random_addresses()
            
            print(f"Creating {len(addresses)} addresses on FortiManager...")
            for address in addresses:
                name = address['name']
                subnet = address['subnet']
                comment = address['comment']
                color = address.get('color')
                
                print(f"Creating address: {name} ({subnet})...")
                code, resp = create_firewall_address(fmg, name, subnet, comment, color)
                
                if code == 0:
                    print(f"  Success: {name} created successfully.")
                else:
                    print(f"  Failure: Unable to create {name}. Code: {code}")
            
            print("Operation completed.")
                
        finally:
            fmg.commit_changes(ADOM)
            fmg.unlock_adom(ADOM)

if __name__ == "__main__":
    main()
