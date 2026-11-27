
import ipaddress
import platform
import subprocess
import re


def network_diagnostics():

    print("\n" + "=" * 60)
    print("                  NETWORK DIAGNOSTICS")
    print("=" * 60)

    try:
        # Take IPv4 address from the user
        ip_input = input("\nEnter IPv4 Address to Ping: ").strip()

        if not ip_input:
            print("\nError: IP address cannot be empty.")
            return

        # Validate IPv4 address
        ip = ipaddress.IPv4Address(ip_input)

        print("\nStarting network diagnostic...")
        print(f"Target IP Address : {ip}")
        print("Packets           : 4")
        print("-" * 60)

        # Select ping command according to operating system
        system = platform.system().lower()

        if system == "windows":
            command = ["ping", "-n", "4", "-w", "1000", str(ip)]

        elif system in ["linux", "darwin"]:
            command = ["ping", "-c", "4", str(ip)]

        else:
            print("\nError: Your operating system is not supported.")
            return

        # Execute ping command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15
        )

        output = result.stdout + result.stderr

        print("\nPING OUTPUT")
        print("-" * 60)
        print(output if output.strip() else "No response received.")

        # Extract packet statistics
        sent = received = lost = None
        packet_loss = None

        # Windows output format
        windows_match = re.search(
            r"Sent\s*=\s*(\d+),\s*Received\s*=\s*(\d+),\s*Lost\s*=\s*(\d+)",
            output,
            re.IGNORECASE
        )

        # Linux/macOS output format
        unix_match = re.search(
            r"(\d+)\s+packets transmitted,\s*"
            r"(\d+)\s+(?:packets )?received",
            output,
            re.IGNORECASE
        )

        if windows_match:
            sent = int(windows_match.group(1))
            received = int(windows_match.group(2))
            lost = int(windows_match.group(3))

        elif unix_match:
            sent = int(unix_match.group(1))
            received = int(unix_match.group(2))
            lost = sent - received

        if sent is not None and sent > 0:

            packet_loss = (lost / sent) * 100

            print("\n" + "=" * 60)
            print("                 DIAGNOSTIC SUMMARY")
            print("=" * 60)

            print(f"\nTarget IP       : {ip}")
            print(f"Packets Sent    : {sent}")
            print(f"Packets Received: {received}")
            print(f"Packets Lost    : {lost}")
            print(f"Packet Loss     : {packet_loss:.2f}%")

            if received > 0:
                print("\nNetwork Status  : Destination is reachable.")
            else:
                print("\nNetwork Status  : No ping replies received.")

        else:
            print("\nCould not extract packet statistics from the system output.")

        # Extract response time statistics
        windows_time = re.search(
            r"Minimum\s*=\s*(\d+)ms,\s*Maximum\s*=\s*(\d+)ms,\s*Average\s*=\s*(\d+)ms",
            output,
            re.IGNORECASE
        )

        unix_time = re.search(
            r"(?:rtt|round-trip).*?=\s*"
            r"([\d.]+)/([\d.]+)/([\d.]+)",
            output,
            re.IGNORECASE
        )

        if windows_time:
            print("\nResponse Time")
            print("-" * 60)
            print(f"Minimum : {windows_time.group(1)} ms")
            print(f"Maximum : {windows_time.group(2)} ms")
            print(f"Average : {windows_time.group(3)} ms")

        elif unix_time:
            print("\nResponse Time")
            print("-" * 60)
            print(f"Minimum : {unix_time.group(1)} ms")
            print(f"Average : {unix_time.group(2)} ms")
            print(f"Maximum : {unix_time.group(3)} ms")

        else:
            print("\nResponse time statistics are unavailable.")

        print("\n" + "=" * 60)
        print("             DIAGNOSTICS COMPLETED")
        print("=" * 60)

        print(
            "\nNote: A failed ping does not always mean the device is offline. "
            "A firewall or network configuration may block ICMP requests."
        )

    except ipaddress.AddressValueError:
        print("\nError: Please enter a valid IPv4 address.")

    except subprocess.TimeoutExpired:
        print("\nError: Ping operation timed out.")

    except FileNotFoundError:
        print("\nError: Ping utility was not found on this system.")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


if __name__ == "__main__":
    network_diagnostics()
