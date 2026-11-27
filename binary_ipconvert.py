
import ipaddress


def convert_to_binary(ip):
    """
    Converts an IPv4 address into 32-bit binary format.
    """
    return ".".join(
        format(int(octet), "08b")
        for octet in str(ip).split(".")
    )


def binary_ip_converter():

    print("\n" + "=" * 55)
    print("                 BINARY IP CONVERTER")
    print("=" * 55)

    try:
        ip = input("\nEnter IPv4 Address: ").strip()
        subnet = input("Enter CIDR Prefix or Subnet Mask: ").strip()

        if not ip or not subnet:
            print("\nError: Both fields are required!")
            return
        address = ipaddress.IPv4Address(ip)

        network = ipaddress.IPv4Network(
            f"{address}/{subnet}",
            strict=False
        )
        ip_binary = convert_to_binary(address)
        mask_binary = convert_to_binary(network.netmask)
        network_binary = convert_to_binary(network.network_address)

        ip_bits = ip_binary.replace(".", "")
        prefix = network.prefixlen

        network_bits = ip_bits[:prefix]
        host_bits = ip_bits[prefix:]

        print("\n" + "-" * 55)
        print("                 BINARY RESULTS")
        print("-" * 55)

        print(f"\nIP Address       : {address}")
        print(f"Binary IP        : {ip_binary}")

        print(f"\nSubnet Mask      : {network.netmask}")
        print(f"Binary Mask      : {mask_binary}")

        print(f"\nNetwork ID       : {network.network_address}")
        print(f"Binary Network   : {network_binary}")

        print("\n" + "-" * 55)
        print("             NETWORK / HOST BREAKDOWN")
        print("-" * 55)

        print(f"\nCIDR Prefix      : /{prefix}")
        print(f"Network Bits     : {prefix}")
        print(f"Host Bits        : {32 - prefix}")

        print(f"\nNetwork Portion  : {network_bits if network_bits else 'None'}")
        print(f"Host Portion     : {host_bits if host_bits else 'None'}")

        print("\n" + "-" * 55)
        print("                BITWISE AND OPERATION")
        print("-" * 55)

        print(f"\nIP Address       : {ip_binary}")
        print(f"Subnet Mask      : {mask_binary}")
        print("-" * 55)
        print(f"Network ID       : {network_binary}")

        print("\n" + "=" * 55)
        print("          BINARY CONVERSION COMPLETED!")
        print("=" * 55)

    except ipaddress.AddressValueError:
        print("\nError: Invalid IPv4 address!")

    except (ipaddress.NetmaskValueError, ValueError):
        print("\nError: Invalid CIDR prefix or subnet mask!")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


if __name__ == "__main__":
    binary_ip_converter()
