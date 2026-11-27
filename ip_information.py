
import ipaddress


def get_ip_class(ip):
    """
    Identifies the traditional IPv4 address class.
    """

    first_octet = int(str(ip).split(".")[0])

    if 1 <= first_octet <= 126:
        return "Class A"

    elif 128 <= first_octet <= 191:
        return "Class B"

    elif 192 <= first_octet <= 223:
        return "Class C"

    elif 224 <= first_octet <= 239:
        return "Class D (Multicast)"

    elif 240 <= first_octet <= 255:
        return "Class E (Experimental/Reserved)"

    else:
        return "Reserved / Special"


def get_address_type(ip):
    """
    Identifies whether an IPv4 address is private,
    public, or belongs to a special-purpose range.
    """

    private_networks = [
        ipaddress.IPv4Network("10.0.0.0/8"),
        ipaddress.IPv4Network("172.16.0.0/12"),
        ipaddress.IPv4Network("192.168.0.0/16")
    ]
    for network in private_networks:
        if ip in network:
            return "Private"

    if ip.is_loopback:
        return "Special (Loopback)"

    elif ip.is_link_local:
        return "Special (Link-Local)"

    elif ip.is_multicast:
        return "Special (Multicast)"

    elif ip.is_unspecified:
        return "Special (Unspecified)"

    elif ip.is_reserved:
        return "Special (Reserved)"

    elif ip.is_global:
        return "Public"

    else:
        return "Special / Non-global"


def ip_information():

    print("\n" + "=" * 60)
    print("             IP ADDRESS CLASS & INFORMATION")
    print("=" * 60)

    try:
        ip_input = input("\nEnter IPv4 Address: ").strip()

        if not ip_input:
            print("\nError: IP address cannot be empty.")
            return

        ip = ipaddress.IPv4Address(ip_input)

        address_class = get_ip_class(ip)
        address_type = get_address_type(ip)
        print("\n" + "-" * 60)
        print("                  IP INFORMATION")
        print("-" * 60)

        print(f"\nIP Address          : {ip}")
        print(f"IP Version          : IPv{ip.version}")
        print(f"Address Class       : {address_class}")
        print(f"Address Type        : {address_type}")

        print("\n" + "-" * 60)
        print("                 NETWORK PROPERTIES")
        print("-" * 60)

        print(f"\nPrivate Address     : {'Yes' if address_type == 'Private' else 'No'}")
        print(f"Public Address      : {'Yes' if address_type == 'Public' else 'No'}")
        print(f"Loopback Address    : {'Yes' if ip.is_loopback else 'No'}")
        print(f"Link-Local Address  : {'Yes' if ip.is_link_local else 'No'}")
        print(f"Multicast Address   : {'Yes' if ip.is_multicast else 'No'}")
        print(f"Reserved Address    : {'Yes' if ip.is_reserved else 'No'}")
        print(f"Unspecified Address : {'Yes' if ip.is_unspecified else 'No'}")
        print(f"Globally Reachable  : {'Yes' if ip.is_global else 'No'}")

        print("\n" + "-" * 60)
        print("                  ADDRESS DETAILS")
        print("-" * 60)

        print(f"\nBinary Address      : " + ".".join(
            format(int(octet), "08b")
            for octet in str(ip).split(".")
        ))

        print(f"Integer Value       : {int(ip)}")

        print("\n" + "=" * 60)
        print("             IP INFORMATION COMPLETED")
        print("=" * 60)

    except ipaddress.AddressValueError:
        print("\nError: Please enter a valid IPv4 address.")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


if __name__ == "__main__":
    ip_information()
