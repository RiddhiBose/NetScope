
import ipaddress


def calculate_required_prefix(hosts):
    """
    Calculates the smallest IPv4 subnet prefix
    capable of accommodating the requested hosts.
    """

    if hosts <= 0:
        raise ValueError("Host requirement must be greater than zero.")
    if hosts <= 2:
        return 31
    host_bits = (hosts + 2 - 1).bit_length()

    if host_bits > 32:
        raise ValueError("Host requirement is too large.")

    return 32 - host_bits


def calculate_vlsm():

    print("\n" + "=" * 60)
    print("                 VLSM SUBNET CALCULATOR")
    print("=" * 60)

    try:
        parent_input = input(
            "\nEnter Parent Network (Example: 192.168.1.0/24): "
        ).strip()

        if not parent_input:
            print("\nError: Parent network is required.")
            return

        parent_network = ipaddress.IPv4Network(
            parent_input,
            strict=False
        )

        count_input = input(
            "Enter Number of Subnets/Departments: "
        ).strip()

        if not count_input.isdigit():
            print("\nError: Enter a valid positive number.")
            return

        count = int(count_input)

        if count <= 0:
            print("\nError: At least one subnet is required.")
            return

        departments = []

        print("\nEnter Department Details")
        print("-" * 60)

        for i in range(count):

            print(f"\nDepartment {i + 1}")

            name = input("Department Name: ").strip()

            if not name:
                print("Error: Department name cannot be empty.")
                return

            hosts_input = input("Required Hosts: ").strip()

            if not hosts_input.isdigit():
                print("Error: Enter a valid host count.")
                return

            hosts = int(hosts_input)

            if hosts <= 0:
                print("Error: Host count must be greater than zero.")
                return

            prefix = calculate_required_prefix(hosts)

            departments.append({
                "name": name,
                "hosts": hosts,
                "prefix": prefix
            })
        departments.sort(
            key=lambda x: x["hosts"],
            reverse=True
        )
        current_address = int(parent_network.network_address)
        parent_end = int(parent_network.broadcast_address)

        results = []

        for department in departments:

            prefix = department["prefix"]

            subnet_size = 2 ** (32 - prefix)

            aligned_address = (
                (current_address + subnet_size - 1)
                // subnet_size
            ) * subnet_size

            subnet_end = aligned_address + subnet_size - 1

            if (
                aligned_address < int(parent_network.network_address)
                or subnet_end > parent_end
            ):
                print("\nError: Insufficient address space!")
                print(
                    f"Cannot allocate subnet for "
                    f"{department['name']}."
                )
                return

            subnet = ipaddress.IPv4Network(
                (aligned_address, prefix)
            )

            # Calculate usable host information
            total_addresses = subnet.num_addresses

            if prefix <= 30:
                usable_hosts = total_addresses - 2
                first_usable = subnet.network_address + 1
                last_usable = subnet.broadcast_address - 1

            elif prefix == 31:
                usable_hosts = 2
                first_usable = subnet.network_address
                last_usable = subnet.broadcast_address

            else:
                usable_hosts = 1
                first_usable = subnet.network_address
                last_usable = subnet.network_address

            results.append({
                "name": department["name"],
                "requested": department["hosts"],
                "network": subnet,
                "mask": subnet.netmask,
                "broadcast": subnet.broadcast_address,
                "first": first_usable,
                "last": last_usable,
                "total": total_addresses,
                "usable": usable_hosts
            })

            # Move to the next available address
            current_address = subnet_end + 1

        # Display allocation results
        print("\n" + "=" * 60)
        print("                 VLSM ALLOCATION RESULTS")
        print("=" * 60)

        print(f"\nParent Network : {parent_network}")
        print(f"Parent Mask    : {parent_network.netmask}")

        for i, result in enumerate(results, start=1):

            print("\n" + "-" * 60)
            print(f"SUBNET {i}: {result['name'].upper()}")
            print("-" * 60)

            print(f"Requested Hosts : {result['requested']}")
            print(f"Network ID      : {result['network']}")
            print(f"CIDR Prefix     : /{result['network'].prefixlen}")
            print(f"Subnet Mask     : {result['mask']}")
            print(f"Broadcast ID    : {result['broadcast']}")
            print(f"First Usable IP : {result['first']}")
            print(f"Last Usable IP  : {result['last']}")
            print(f"Total Addresses : {result['total']}")
            print(f"Usable Hosts    : {result['usable']}")

        # Verify that no allocated networks overlap
        print("\n" + "=" * 60)
        print("               ALLOCATION VERIFICATION")
        print("=" * 60)

        overlap_found = False

        for i in range(len(results)):
            for j in range(i + 1, len(results)):
                if results[i]["network"].overlaps(
                    results[j]["network"]
                ):
                    overlap_found = True

        if not overlap_found:
            print("\nAll allocated subnets are non-overlapping.")
        else:
            print("\nWarning: Overlapping subnets detected.")

        allocated = sum(r["total"] for r in results)

        print(f"\nParent Network Addresses : {parent_network.num_addresses}")
        print(f"Allocated Addresses      : {allocated}")
        print(
            f"Remaining Addresses      : "
            f"{parent_network.num_addresses - allocated}"
        )

        print("\nVLSM calculation completed successfully!")

    except ipaddress.AddressValueError:
        print("\nError: Invalid IPv4 address.")

    except (ipaddress.NetmaskValueError, ValueError) as error:
        print(f"\nError: {error}")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


if __name__ == "__main__":
    calculate_vlsm()
