
import ipaddress
import json
import os
from datetime import datetime

# ==========================================
# 1. NETWORK CONFIGURATION
# ==========================================

main_network = ipaddress.ip_network("192.168.1.0/24")
subnets = list(main_network.subnets(new_prefix=25))

departments = {
    "Development": subnets[0],
    "Finance/HR": subnets[1]
}

devices = {
    "Dev-PC1": "192.168.1.10",
    "Dev-PC2": "192.168.1.20",
    "Finance-PC1": "192.168.1.130",
    "HR-PC1": "192.168.1.140"
}


# ==========================================
# 2. SECURITY POLICY STORAGE
# ==========================================

POLICY_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "security_policies.json"
)


def load_security_policies():
    """Load saved security policies from the JSON file."""

    if os.path.exists(POLICY_FILE):
        try:
            with open(POLICY_FILE, "r") as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read policy file. Starting with empty policies.")

    return {}


def save_security_policies():
    """Save security policies to the JSON file."""

    with open(POLICY_FILE, "w") as file:
        json.dump(security_policies, file, indent=4)


security_policies = load_security_policies()


# ==========================================
# 3. NETWORK DETAILS
# ==========================================

def display_network_details():

    print("\n========== NETWORK DETAILS ==========")

    for department, network in departments.items():

        hosts = list(network.hosts())

        print(f"\nDepartment: {department}")
        print("Network:", network.network_address)
        print("Subnet Mask:", network.netmask)
        print("Broadcast:", network.broadcast_address)
        print("Usable Hosts:", len(hosts))

        if hosts:
            print("IP Range:", hosts[0], "-", hosts[-1])


# ==========================================
# 4. DEVICE DETAILS
# ==========================================

def display_devices():

    print("\n========== DEVICE ASSIGNMENTS ==========")

    for device, ip in devices.items():
        print(device, ":", ip)


# ==========================================
# 5. FIND DEVICE DEPARTMENT
# ==========================================

def get_department(ip):

    ip = ipaddress.ip_address(ip)

    for department, network in departments.items():

        if ip in network:
            return department

    return None


# ==========================================
# 6. CONNECTIVITY TEST
# ==========================================

def check_connectivity(source, destination):

    print("\n========== CONNECTIVITY TEST ==========")

    if source not in devices or destination not in devices:
        print("Error: Device not found!")
        return

    source_ip = devices[source]
    destination_ip = devices[destination]

    source_dept = get_department(source_ip)
    destination_dept = get_department(destination_ip)

    print("Source:", source, source_ip)
    print("Destination:", destination, destination_ip)

    if source_dept is None or destination_dept is None:
        print("ERROR: Device is not assigned to a department!")
        return

    # Create a unique key for this department pair
    policy_key = f"{source_dept}|{destination_dept}"

    # Check whether a custom policy exists
    if policy_key in security_policies:

        allowed = security_policies[policy_key]["allowed"]

        print(
            "Security Policy:",
            "ALLOW" if allowed else "DENY"
        )

    else:

        # Default policy:
        # Same department = ALLOW
        # Different departments = DENY

        allowed = source_dept == destination_dept

        print("Security Policy: DEFAULT")

    if allowed:
        print("\nPING SUCCESSFUL!")
        print("Communication is allowed.")

    else:
        print("\nPING BLOCKED!")
        print("Communication denied by security policy.")


# ==========================================
# 7. ADD SECURITY POLICY
# ==========================================

def add_security_policy():

    print("\n========== ADD SECURITY POLICY ==========")

    department_list = list(departments.keys())

    for i, department in enumerate(department_list, 1):
        print(f"{i}. {department}")

    try:
        source_choice = int(input("\nSelect source department: "))
        destination_choice = int(input("Select destination department: "))

        if not (1 <= source_choice <= len(department_list)):
            print("Invalid source department!")
            return

        if not (1 <= destination_choice <= len(department_list)):
            print("Invalid destination department!")
            return

        source = department_list[source_choice - 1]
        destination = department_list[destination_choice - 1]

        print("\n1. ALLOW communication")
        print("2. DENY communication")

        action = input("Choose action: ")

        if action == "1":
            allowed = True

        elif action == "2":
            allowed = False

        else:
            print("Invalid action!")
            return

        policy_key = f"{source}|{destination}"

        # Store policy and timestamp
        security_policies[policy_key] = {
            "allowed": allowed,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save policy permanently
        save_security_policies()

        print("\nSecurity policy successfully updated!")
        print(f"{source} -> {destination}")
        print("Action:", "ALLOW" if allowed else "DENY")
        print("Policy saved successfully!")

    except ValueError:
        print("Please enter valid numbers!")


# ==========================================
# 8. VIEW SECURITY POLICIES
# ==========================================

def view_security_policies():

    print("\n========== SECURITY POLICIES ==========")

    if not security_policies:
        print("No custom policies configured.")
        print("Default policy: Same department ALLOW, different departments DENY.")
        return

    for key, details in security_policies.items():

        source, destination = key.split("|", 1)

        action = "ALLOW" if details["allowed"] else "DENY"

        print(f"\nSource: {source}")
        print(f"Destination: {destination}")
        print(f"Action: {action}")
        print(f"Updated: {details.get('updated_at', 'Unknown')}")


# ==========================================
# 9. DELETE SECURITY POLICY
# ==========================================

def delete_security_policy():

    print("\n========== DELETE SECURITY POLICY ==========")

    view_security_policies()

    if not security_policies:
        return

    department_list = list(departments.keys())

    try:
        source_choice = int(input("\nSelect source department (1-2): "))
        destination_choice = int(input("Select destination department (1-2): "))

        if not (1 <= source_choice <= len(department_list)):
            print("Invalid source!")
            return

        if not (1 <= destination_choice <= len(department_list)):
            print("Invalid destination!")
            return

        source = department_list[source_choice - 1]
        destination = department_list[destination_choice - 1]

        policy_key = f"{source}|{destination}"

        if policy_key in security_policies:

            del security_policies[policy_key]

            save_security_policies()

            print("Security policy deleted successfully!")

        else:
            print("No matching policy found!")

    except ValueError:
        print("Please enter valid numbers!")


# ==========================================
# 10. SECURITY POLICY MENU
# ==========================================

def security_policy_menu():

    while True:

        print("\n========== SECURITY MANAGEMENT ==========")
        print("1. Add Security Policy")
        print("2. View Security Policies")
        print("3. Delete Security Policy")
        print("4. Back to Main Menu")

        choice = input("\nEnter choice: ")

        if choice == "1":
            add_security_policy()

        elif choice == "2":
            view_security_policies()

        elif choice == "3":
            delete_security_policy()

        elif choice == "4":
            break

        else:
            print("Invalid choice!")


# ==========================================
# 11. CUSTOM SUBNET CALCULATOR
# ==========================================

def calculate_custom_subnet():

    print("\n========== CUSTOM SUBNET CALCULATOR ==========")

    try:
        ip = input("Enter IP address or network: ")
        prefix = input("Enter prefix length: ")

        network = ipaddress.ip_network(
            f"{ip}/{prefix}", strict=False
        )

        hosts = list(network.hosts())

        print("\nNetwork Address:", network.network_address)
        print("Subnet Mask:", network.netmask)
        print("Broadcast Address:", network.broadcast_address)
        print("Prefix Length:", network.prefixlen)
        print("Total IP Addresses:", network.num_addresses)
        print("Usable Hosts:", len(hosts))

        if hosts:
            print("First Usable IP:", hosts[0])
            print("Last Usable IP:", hosts[-1])

    except ValueError:
        print("Invalid IP address or prefix!")


# ==========================================
# 12. MAIN MENU
# ==========================================

while True:

    print("\n========== SECURE STARTUP LAN ==========")
    print("1. Display Subnet Details")
    print("2. Display Device IP Addresses")
    print("3. Test Network Connectivity")
    print("4. Security Policy Management")
    print("5. Custom Subnet Calculator")
    print("6. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        display_network_details()

    elif choice == "2":
        display_devices()

    elif choice == "3":

        print("\nAvailable Devices:")

        for device in devices:
            print(device)

        source = input("\nEnter source device: ")
        destination = input("Enter destination device: ")

        check_connectivity(source, destination)

    elif choice == "4":
        security_policy_menu()

    elif choice == "5":
        calculate_custom_subnet()

    elif choice == "6":
        print("Exiting Secure Startup LAN Simulator.")
        break

    else:
        print("Invalid choice!")
