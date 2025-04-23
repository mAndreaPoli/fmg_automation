# FortiManager Automation Tool

Automation tool for creating address objects on FortiManager using the pyFMG API.

## Description

This project automates the creation of network address objects on FortiManager using the pyFMG library. The tool can operate in two ways:
- **Automatic mode**: generates random addresses
- **CSV mode**: imports addresses from a CSV file

## Prerequisites

- Python 3.6+
- Access to a FortiManager with administrative rights
- Required libraries:
  - pyfmg
  - python-dotenv
  - ipaddress (included in Python standard library)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/mAndreaPoli/fmg_automation.git
   cd fmg_automation
   ```

2. Install dependencies:
   ```bash
   pip install pyfmg python-dotenv
   ```

3. Configure your FortiManager connection information (see Configuration section).

## Configuration

Create a `.env` file at the root of the project with the following parameters:

```
FMG_IP = <fortimanager_ip_address>
USERNAME = <username>
PASSWORD = <password>
ADOM = <target_adom>
```

Example:
```
FMG_IP = 192.168.0.3
USERNAME = admin
PASSWORD = password123
ADOM = root
```

**Security note**: The `.env` file is excluded from version control via `.gitignore`. Never commit this file containing credentials.

## Usage

### Automatic mode (random address generation)

To generate and create 10 random addresses (default behavior):

```bash
python main.py
```

### CSV mode (importing addresses from a file)

To import addresses from a CSV file:

```bash
python main.py path/to/your/file.csv
```

## CSV File Format

The CSV file must contain the following columns:

| Column   | Required | Description |
|----------|----------|-------------|
| name     | No (default value: host_XXXX) | Name of the address object |
| subnet   | Yes | Subnet in CIDR format (e.g., 192.168.1.0/24) |
| comment  | No | Comment for the address object |
| color    | No | Color number (1-32) |

Example CSV file:
```csv
name,subnet,comment,color
host_0001,192.168.1.0/24,"Primary LAN Network",5
host_0002,10.0.1.0/24,"VPN Network",7
```

## Features

- Creation of network address objects on FortiManager
- Automatic management of ADOM locking/unlocking
- Validation of subnets in CIDR format
- Automatic or defined color assignment
- Operation logging
- Error handling for robust integrations

## Technical Details

The script performs the following operations:
1. Connects to FortiManager
2. Locks the specified ADOM
3. Imports addresses from a CSV or generates random addresses
4. Creates the address objects on FortiManager
5. Validates the changes
6. Unlocks the ADOM

## Advanced Usage Examples

### Creating addresses with specific colors

```csv
name,subnet,comment,color
Guest_Network,192.168.10.0/24,"Guest Network",8
```

## Troubleshooting

- **Connection error**: Verify that the connection information in the `.env` file is correct
- **ADOM error**: Verify that the specified ADOM exists and that the user has access rights
- **CSV error**: Make sure the CSV format is correct and that the 'subnet' column is present

## License

This project is distributed under the MIT license. See the `LICENSE` file for more details.