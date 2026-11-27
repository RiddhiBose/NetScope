
import tkinter as tk
from tkinter import ttk, messagebox
import ipaddress
import subprocess
import platform
import threading
import re


# ============================================================
# NETSCOPE - DESKTOP NETWORKING TOOLKIT
# Built using Python Tkinter
# ============================================================

BG = "#0B1120"
SIDEBAR = "#111B2E"
PANEL = "#162238"
INPUT_BG = "#0D1729"
ACCENT = "#00D6A3"
CYAN = "#38BDF8"
TEXT = "#E5EDF7"
MUTED = "#8FA3BD"
RED = "#FB7185"
BORDER = "#253650"


class NetScope:

    def __init__(self, root):

        self.root = root
        self.root.title("NetScope | Network Administration Toolkit")
        self.root.geometry("1100x720")
        self.root.minsize(950, 620)
        self.root.configure(bg=BG)

        self.current_page = "Subnet Calculator"

        self.setup_styles()
        self.create_layout()
        self.show_page("Subnet Calculator")

    # ========================================================
    # STYLES
    # ========================================================

    def setup_styles(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=INPUT_BG,
            foreground=TEXT,
            fieldbackground=INPUT_BG,
            rowheight=30,
            borderwidth=0,
            font=("Consolas", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=PANEL,
            foreground=ACCENT,
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", "#24435B")],
            foreground=[("selected", "white")]
        )

    # ========================================================
    # MAIN LAYOUT
    # ========================================================

    def create_layout(self):

        # Main container
        container = tk.Frame(self.root, bg=BG)
        container.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(
            container,
            bg=SIDEBAR,
            width=245
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Main content
        self.content = tk.Frame(container, bg=BG)
        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_sidebar()
        self.create_header()

        # Dynamic page area
        self.page_area = tk.Frame(
            self.content,
            bg=BG
        )
        self.page_area.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(15, 20)
        )

    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        logo = tk.Frame(self.sidebar, bg=SIDEBAR)
        logo.pack(fill="x", padx=22, pady=(30, 35))

        tk.Label(
            logo,
            text="◈  NETSCOPE",
            font=("Segoe UI", 22, "bold"),
            fg=ACCENT,
            bg=SIDEBAR
        ).pack(anchor="w")

        tk.Label(
            logo,
            text="NETWORKING TOOLKIT",
            font=("Segoe UI", 8, "bold"),
            fg=MUTED,
            bg=SIDEBAR
        ).pack(anchor="w", pady=(5, 0))

        tk.Label(
            self.sidebar,
            text="MAIN MENU",
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=SIDEBAR
        ).pack(anchor="w", padx=22, pady=(0, 12))

        self.nav_buttons = {}

        options = [
            ("Subnet Calculator", "01"),
            ("Binary IP Converter", "02"),
            ("VLSM Calculator", "03"),
            ("Network Diagnostics", "04"),
            ("IP Information", "05")
        ]

        for name, number in options:

            button = tk.Button(
                self.sidebar,
                text=f"   {number}    {name}",
                font=("Segoe UI", 10),
                bg=SIDEBAR,
                fg=TEXT,
                activebackground=PANEL,
                activeforeground=ACCENT,
                bd=0,
                relief="flat",
                anchor="w",
                cursor="hand2",
                padx=15,
                pady=13,
                command=lambda n=name: self.show_page(n)
            )

            button.pack(fill="x", padx=10, pady=2)

            self.nav_buttons[name] = button

        # Sidebar bottom
        bottom = tk.Frame(self.sidebar, bg=SIDEBAR)
        bottom.pack(side="bottom", fill="x", padx=22, pady=25)

        tk.Frame(
            bottom,
            bg=BORDER,
            height=1
        ).pack(fill="x", pady=(0, 15))

        tk.Label(
            bottom,
            text="●  SYSTEM READY",
            font=("Consolas", 9, "bold"),
            fg=ACCENT,
            bg=SIDEBAR
        ).pack(anchor="w")

        tk.Label(
            bottom,
            text="NetScope v1.0.0",
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=SIDEBAR
        ).pack(anchor="w", pady=(6, 0))

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.content,
            bg=BG,
            height=75
        )
        header.pack(fill="x", padx=25, pady=(20, 0))
        header.pack_propagate(False)

        self.header_title = tk.Label(
            header,
            text="Subnet Calculator",
            font=("Segoe UI", 19, "bold"),
            fg=TEXT,
            bg=BG
        )
        self.header_title.pack(side="left", anchor="center")

        tk.Label(
            header,
            text="● ONLINE",
            font=("Consolas", 9, "bold"),
            fg=ACCENT,
            bg=BG
        ).pack(side="right", anchor="center")

        tk.Frame(
            self.content,
            bg=BORDER,
            height=1
        ).pack(fill="x", padx=25)

    # ========================================================
    # COMMON UI HELPERS
    # ========================================================

    def clear_page(self):

        for widget in self.page_area.winfo_children():
            widget.destroy()

    def show_page(self, page):

        self.current_page = page
        self.header_title.config(text=page)

        for name, button in self.nav_buttons.items():

            if name == page:
                button.config(
                    bg=PANEL,
                    fg=ACCENT
                )
            else:
                button.config(
                    bg=SIDEBAR,
                    fg=TEXT
                )

        self.clear_page()

        pages = {
            "Subnet Calculator": self.subnet_page,
            "Binary IP Converter": self.binary_page,
            "VLSM Calculator": self.vlsm_page,
            "Network Diagnostics": self.diagnostics_page,
            "IP Information": self.information_page
        }

        pages[page]()

    def create_title(self, title, description):

        tk.Label(
            self.page_area,
            text=title,
            font=("Segoe UI", 16, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(anchor="w")

        tk.Label(
            self.page_area,
            text=description,
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=BG
        ).pack(anchor="w", pady=(5, 15))

    def create_card(self, parent=None):

        if parent is None:
            parent = self.page_area

        card = tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        return card

    def create_input(self, parent, label, default=""):

        wrapper = tk.Frame(parent, bg=PANEL)
        wrapper.pack(fill="x", padx=18, pady=8)

        tk.Label(
            wrapper,
            text=label,
            font=("Segoe UI", 9, "bold"),
            fg=MUTED,
            bg=PANEL
        ).pack(anchor="w", pady=(0, 6))

        entry = tk.Entry(
            wrapper,
            font=("Consolas", 11),
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground=ACCENT,
            relief="flat",
            bd=0
        )

        entry.pack(fill="x", ipady=10)

        if default:
            entry.insert(0, default)

        return entry

    def create_button(self, parent, text, command):

        button = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT,
            fg="#07151A",
            activebackground="#00B98D",
            activeforeground="#07151A",
            bd=0,
            relief="flat",
            padx=20,
            pady=11,
            cursor="hand2",
            command=command
        )

        return button


    def create_output(self, parent=None, height=12):

        if parent is None:
            parent = self.page_area

        card = self.create_card(parent)

        # FIX: Actually display the output card in the window
        card.pack(
            fill="both",
            expand=True,
            pady=(0, 10)
        )

        tk.Label(
            card,
            text="▸  TERMINAL OUTPUT",
            font=("Consolas", 10, "bold"),
            fg=ACCENT,
            bg=PANEL
        ).pack(anchor="w", padx=15, pady=(12, 5))

        output = tk.Text(
            card,
            height=height,
            bg=INPUT_BG,
            fg=TEXT,
            font=("Consolas", 10),
            insertbackground=ACCENT,
            relief="flat",
            bd=0,
            wrap="word",
            padx=12,
            pady=10
        )

        output.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        output.config(state="disabled")

        return card, output

    def write_output(self, widget, text):

        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("end", text)
        widget.config(state="disabled")

    # ========================================================
    # 1. SUBNET CALCULATOR
    # ========================================================

    def subnet_page(self):

        self.create_title(
            "IPv4 Subnet Calculator",
            "Calculate network information from an IPv4 address and subnet mask."
        )

        card = self.create_card()
        card.pack(fill="x", pady=(0, 15))

        self.subnet_ip = self.create_input(
            card, "IP ADDRESS", "192.168.1.10"
        )

        self.subnet_mask = self.create_input(
            card, "CIDR PREFIX OR SUBNET MASK", "24"
        )

        self.create_button(
            card,
            "CALCULATE SUBNET  →",
            self.calculate_subnet
        ).pack(anchor="w", padx=18, pady=15)

        _, self.subnet_output = self.create_output(height=13)

        self.write_output(
            self.subnet_output,
            "NetScope Subnet Calculator\n"
            "---------------------------------------------\n"
            "Enter an IPv4 address and subnet mask.\n"
            "Click CALCULATE SUBNET to begin."
        )

    def calculate_subnet(self):

        try:

            ip = ipaddress.IPv4Address(
                self.subnet_ip.get().strip()
            )

            subnet = self.subnet_mask.get().strip()

            network = ipaddress.IPv4Network(
                f"{ip}/{subnet}",
                strict=False
            )

            total = network.num_addresses

            if network.prefixlen <= 30:
                usable = total - 2
                first = network.network_address + 1
                last = network.broadcast_address - 1

            elif network.prefixlen == 31:
                usable = 2
                first = network.network_address
                last = network.broadcast_address

            else:
                usable = 1
                first = network.network_address
                last = network.network_address

            result = f"""
NETSCOPE // SUBNET CALCULATION
=============================================

IP ADDRESS INFORMATION

IP Address       : {ip}
Subnet Mask      : {network.netmask}
CIDR Prefix      : /{network.prefixlen}

NETWORK INFORMATION

Network ID       : {network.network_address}
Broadcast ID     : {network.broadcast_address}

HOST INFORMATION

First Usable IP  : {first}
Last Usable IP   : {last}

Total Addresses  : {total}
Usable Hosts     : {usable}

=============================================
SUBNET CALCULATION COMPLETED SUCCESSFULLY.
"""

            self.write_output(self.subnet_output, result)

        except Exception as error:
            self.write_output(
                self.subnet_output,
                f"ERROR: {error}"
            )

    # ========================================================
    # 2. BINARY IP CONVERTER
    # ========================================================

    def binary_page(self):

        self.create_title(
            "Binary IP Address Converter",
            "Convert IPv4 addresses into binary and examine their network and host bits."
        )

        card = self.create_card()
        card.pack(fill="x", pady=(0, 15))

        self.binary_ip = self.create_input(
            card, "IP ADDRESS", "192.168.1.10"
        )

        self.binary_mask = self.create_input(
            card, "CIDR PREFIX OR SUBNET MASK", "24"
        )

        self.create_button(
            card,
            "CONVERT TO BINARY  →",
            self.calculate_binary
        ).pack(anchor="w", padx=18, pady=15)

        _, self.binary_output = self.create_output(height=15)

        self.write_output(
            self.binary_output,
            "NetScope Binary Converter\n"
            "---------------------------------------------\n"
            "Enter an IPv4 address and prefix to convert."
        )

    def calculate_binary(self):

        try:

            ip = ipaddress.IPv4Address(
                self.binary_ip.get().strip()
            )

            network = ipaddress.IPv4Network(
                f"{ip}/{self.binary_mask.get().strip()}",
                strict=False
            )

            def to_binary(address):

                return ".".join(
                    format(int(octet), "08b")
                    for octet in str(address).split(".")
                )

            ip_binary = to_binary(ip)
            mask_binary = to_binary(network.netmask)
            network_binary = to_binary(network.network_address)

            bits = ip_binary.replace(".", "")

            prefix = network.prefixlen

            network_bits = bits[:prefix]
            host_bits = bits[prefix:]

            result = f"""
NETSCOPE // BINARY CONVERSION
=============================================

IP ADDRESS

Decimal IP  : {ip}
Binary IP   : {ip_binary}

SUBNET MASK

Decimal     : {network.netmask}
Binary      : {mask_binary}

NETWORK ID

Decimal     : {network.network_address}
Binary      : {network_binary}

NETWORK / HOST BREAKDOWN

CIDR Prefix : /{prefix}
Network Bits: {prefix}
Host Bits   : {32 - prefix}

Network Part: {network_bits if network_bits else 'None'}
Host Part   : {host_bits if host_bits else 'None'}

=============================================
BINARY CONVERSION COMPLETED.
"""

            self.write_output(self.binary_output, result)

        except Exception as error:

            self.write_output(
                self.binary_output,
                f"ERROR: {error}"
            )

    # ========================================================
    # 3. VLSM CALCULATOR
    # ========================================================

    def vlsm_page(self):

        self.create_title(
            "VLSM Subnet Calculator",
            "Allocate variable-length subnets according to department host requirements."
        )

        card = self.create_card()
        card.pack(fill="x", pady=(0, 12))

        self.vlsm_parent = self.create_input(
            card,
            "PARENT NETWORK",
            "192.168.1.0/24"
        )

        self.vlsm_count = self.create_input(
            card,
            "NUMBER OF DEPARTMENTS / SUBNETS",
            "4"
        )

        tk.Label(
            card,
            text="Enter one department per line: Department Name, Required Hosts",
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=PANEL
        ).pack(anchor="w", padx=18, pady=(8, 5))

        self.vlsm_details = tk.Text(
            card,
            height=5,
            bg=INPUT_BG,
            fg=TEXT,
            font=("Consolas", 10),
            insertbackground=ACCENT,
            relief="flat",
            bd=0
        )

        self.vlsm_details.pack(
            fill="x",
            padx=18,
            pady=(0, 10)
        )

        self.vlsm_details.insert(
            "1.0",
            "Administration, 100\n"
            "IT Department, 50\n"
            "HR Department, 25\n"
            "Finance, 10"
        )

        self.create_button(
            card,
            "ALLOCATE SUBNETS  →",
            self.calculate_vlsm
        ).pack(anchor="w", padx=18, pady=12)

        _, self.vlsm_output = self.create_output(height=13)

        self.write_output(
            self.vlsm_output,
            "NetScope VLSM Calculator\n"
            "---------------------------------------------\n"
            "Enter a parent network and department details."
        )

    def calculate_vlsm(self):

        try:

            parent = ipaddress.IPv4Network(
                self.vlsm_parent.get().strip(),
                strict=False
            )

            count = int(self.vlsm_count.get().strip())

            if count <= 0:
                raise ValueError("Subnet count must be positive.")

            lines = [
                line.strip()
                for line in self.vlsm_details.get("1.0", "end").splitlines()
                if line.strip()
            ]

            if len(lines) != count:
                raise ValueError(
                    f"Expected {count} department entries, "
                    f"but received {len(lines)}."
                )

            departments = []

            for line in lines:

                parts = line.rsplit(",", 1)

                if len(parts) != 2:
                    raise ValueError(
                        f"Invalid entry: {line}. Use Name, Hosts."
                    )

                name = parts[0].strip()
                hosts = int(parts[1].strip())

                if not name or hosts <= 0:
                    raise ValueError("Names and host counts must be valid.")

                # Find the smallest subnet that accommodates the hosts.
                # Two addresses are reserved for network and broadcast.
                prefix = 32 - (hosts + 2 - 1).bit_length()

                if hosts <= 2:
                    prefix = 31

                if prefix < 0 or prefix > 31:
                    raise ValueError("Invalid host requirement.")

                departments.append({
                    "name": name,
                    "hosts": hosts,
                    "prefix": prefix
                })

            # Largest requirements receive address space first.
            departments.sort(
                key=lambda item: item["hosts"],
                reverse=True
            )

            current = int(parent.network_address)
            parent_end = int(parent.broadcast_address)

            results = []

            for department in departments:

                prefix = department["prefix"]
                size = 2 ** (32 - prefix)

                aligned = (
                    (current + size - 1) // size
                ) * size

                end = aligned + size - 1

                if aligned < int(parent.network_address) or end > parent_end:
                    raise ValueError(
                        f"Insufficient address space for {department['name']}."
                    )

                subnet = ipaddress.IPv4Network(
                    (aligned, prefix)
                )

                if prefix <= 30:
                    first = subnet.network_address + 1
                    last = subnet.broadcast_address - 1
                    usable = subnet.num_addresses - 2
                elif prefix == 31:
                    first = subnet.network_address
                    last = subnet.broadcast_address
                    usable = 2
                else:
                    first = subnet.network_address
                    last = subnet.network_address
                    usable = 1

                results.append({
                    "name": department["name"],
                    "hosts": department["hosts"],
                    "subnet": subnet,
                    "first": first,
                    "last": last,
                    "usable": usable
                })

                current = end + 1

            output = [
                "NETSCOPE // VLSM ALLOCATION",
                "=" * 55,
                f"Parent Network : {parent}",
                f"Parent Mask    : {parent.netmask}",
                "",
                "SUBNET ALLOCATION",
                "-" * 55
            ]

            allocated = 0

            for index, item in enumerate(results, start=1):

                subnet = item["subnet"]
                allocated += subnet.num_addresses

                output.extend([
                    "",
                    f"SUBNET {index}: {item['name'].upper()}",
                    f"Requested Hosts : {item['hosts']}",
                    f"Network ID      : {subnet.network_address}",
                    f"CIDR Prefix     : /{subnet.prefixlen}",
                    f"Subnet Mask     : {subnet.netmask}",
                    f"Broadcast ID    : {subnet.broadcast_address}",
                    f"First Usable IP : {item['first']}",
                    f"Last Usable IP  : {item['last']}",
                    f"Usable Hosts    : {item['usable']}",
                    "-" * 55
                ])

            output.extend([
                "",
                "ALLOCATION SUMMARY",
                f"Parent Addresses    : {parent.num_addresses}",
                f"Allocated Addresses : {allocated}",
                f"Remaining Addresses: {parent.num_addresses - allocated}",
                "",
                "All allocated subnets are non-overlapping.",
                "VLSM ALLOCATION COMPLETED."
            ])

            self.write_output(
                self.vlsm_output,
                "\n".join(output)
            )

        except Exception as error:

            self.write_output(
                self.vlsm_output,
                f"VLSM ERROR: {error}"
            )

    # ========================================================
    # 4. NETWORK DIAGNOSTICS
    # ========================================================

    def diagnostics_page(self):

        self.create_title(
            "Network Diagnostics",
            "Test network reachability using ICMP ping."
        )

        card = self.create_card()
        card.pack(fill="x", pady=(0, 15))

        self.ping_ip = self.create_input(
            card, "TARGET IPv4 ADDRESS", "127.0.0.1"
        )

        self.ping_button = self.create_button(
            card,
            "START DIAGNOSTIC  →",
            self.start_ping
        )

        self.ping_button.pack(anchor="w", padx=18, pady=15)

        _, self.ping_output = self.create_output(height=16)

        self.write_output(
            self.ping_output,
            "NETSCOPE // NETWORK DIAGNOSTICS\n"
            "---------------------------------------------\n"
            "Enter an IPv4 address and start the ping test.\n"
            "The application will send 4 ICMP requests."
        )

    def start_ping(self):

        try:
            ip = ipaddress.IPv4Address(
                self.ping_ip.get().strip()
            )
        except Exception:
            self.write_output(
                self.ping_output,
                "ERROR: Please enter a valid IPv4 address."
            )
            return

        self.ping_button.config(
            state="disabled",
            text="TESTING..."
        )

        self.write_output(
            self.ping_output,
            f"NETSCOPE // NETWORK DIAGNOSTICS\n"
            f"---------------------------------------------\n"
            f"Target IP : {ip}\n"
            f"Packets   : 4\n"
            f"Status    : Running ping test..."
        )

        threading.Thread(
            target=self.run_ping,
            args=(str(ip),),
            daemon=True
        ).start()

    def run_ping(self, ip):

        try:

            system = platform.system().lower()

            if system == "windows":
                command = ["ping", "-n", "4", "-w", "1000", ip]

            elif system in ["linux", "darwin"]:
                command = ["ping", "-c", "4", ip]

            else:
                raise RuntimeError("Unsupported operating system.")

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=15
            )

            output = result.stdout + result.stderr

            windows = re.search(
                r"Sent\s*=\s*(\d+),\s*Received\s*=\s*(\d+),\s*Lost\s*=\s*(\d+)",
                output,
                re.IGNORECASE
            )

            unix = re.search(
                r"(\d+)\s+packets transmitted,\s*(\d+)\s+(?:packets )?received",
                output,
                re.IGNORECASE
            )

            sent = received = lost = None

            if windows:
                sent = int(windows.group(1))
                received = int(windows.group(2))
                lost = int(windows.group(3))

            elif unix:
                sent = int(unix.group(1))
                received = int(unix.group(2))
                lost = sent - received

            if sent is not None and sent > 0:

                loss = lost / sent * 100

                summary = (
                    f"\n\nPACKET STATISTICS\n"
                    f"Packets Sent     : {sent}\n"
                    f"Packets Received : {received}\n"
                    f"Packets Lost     : {lost}\n"
                    f"Packet Loss      : {loss:.2f}%\n"
                    f"Network Status   : "
                    f"{'Reachable' if received else 'No replies received'}\n"
                )

            else:
                summary = "\nPacket statistics could not be parsed.\n"

            windows_time = re.search(
                r"Minimum\s*=\s*(\d+)ms,\s*Maximum\s*=\s*(\d+)ms,\s*Average\s*=\s*(\d+)ms",
                output,
                re.IGNORECASE
            )

            unix_time = re.search(
                r"(?:rtt|round-trip).*?=\s*([\d.]+)/([\d.]+)/([\d.]+)",
                output,
                re.IGNORECASE
            )

            if windows_time:
                summary += (
                    "\nRESPONSE TIME\n"
                    f"Minimum : {windows_time.group(1)} ms\n"
                    f"Maximum : {windows_time.group(2)} ms\n"
                    f"Average : {windows_time.group(3)} ms\n"
                )

            elif unix_time:
                summary += (
                    "\nRESPONSE TIME\n"
                    f"Minimum : {unix_time.group(1)} ms\n"
                    f"Average : {unix_time.group(2)} ms\n"
                    f"Maximum : {unix_time.group(3)} ms\n"
                )

            final_output = (
                f"NETSCOPE // NETWORK DIAGNOSTICS\n"
                f"=============================================\n"
                f"TARGET: {ip}\n\n"
                f"PING OUTPUT\n"
                f"---------------------------------------------\n"
                f"{output}\n"
                f"{summary}\n"
                f"=============================================\n"
                f"DIAGNOSTIC COMPLETED.\n"
                f"Note: Firewalls may block ICMP requests."
            )

        except Exception as error:
            final_output = f"DIAGNOSTIC ERROR: {error}"

        self.root.after(
            0,
            lambda: self.finish_ping(final_output)
        )

    def finish_ping(self, output):

        self.write_output(self.ping_output, output)

        self.ping_button.config(
            state="normal",
            text="START DIAGNOSTIC  →"
        )

    # ========================================================
    # 5. IP ADDRESS INFORMATION
    # ========================================================

    def information_page(self):

        self.create_title(
            "IP Address Class & Information",
            "Identify IPv4 classes, address types and network properties."
        )

        card = self.create_card()
        card.pack(fill="x", pady=(0, 15))

        self.info_ip = self.create_input(
            card, "IPv4 ADDRESS", "192.168.1.1"
        )

        self.create_button(
            card,
            "ANALYZE IP ADDRESS  →",
            self.calculate_information
        ).pack(anchor="w", padx=18, pady=15)

        _, self.info_output = self.create_output(height=15)

        self.write_output(
            self.info_output,
            "NETSCOPE // IP INFORMATION\n"
            "---------------------------------------------\n"
            "Enter an IPv4 address to analyze its properties."
        )

    def calculate_information(self):

        try:

            ip = ipaddress.IPv4Address(
                self.info_ip.get().strip()
            )

            first = int(str(ip).split(".")[0])

            if 1 <= first <= 126:
                ip_class = "Class A"
            elif 128 <= first <= 191:
                ip_class = "Class B"
            elif 192 <= first <= 223:
                ip_class = "Class C"
            elif 224 <= first <= 239:
                ip_class = "Class D (Multicast)"
            elif 240 <= first <= 255:
                ip_class = "Class E (Experimental/Reserved)"
            else:
                ip_class = "Reserved / Special"

            private_ranges = [
                ipaddress.IPv4Network("10.0.0.0/8"),
                ipaddress.IPv4Network("172.16.0.0/12"),
                ipaddress.IPv4Network("192.168.0.0/16")
            ]

            if any(ip in network for network in private_ranges):
                address_type = "Private"
            elif ip.is_loopback:
                address_type = "Special (Loopback)"
            elif ip.is_link_local:
                address_type = "Special (Link-Local)"
            elif ip.is_multicast:
                address_type = "Special (Multicast)"
            elif ip.is_unspecified:
                address_type = "Special (Unspecified)"
            elif ip.is_reserved:
                address_type = "Special (Reserved)"
            elif ip.is_global:
                address_type = "Public"
            else:
                address_type = "Special / Non-global"

            binary = ".".join(
                format(int(octet), "08b")
                for octet in str(ip).split(".")
            )

            result = f"""
NETSCOPE // IP ADDRESS ANALYSIS
=============================================

BASIC INFORMATION

IP Address          : {ip}
IP Version          : IPv{ip.version}
Address Class       : {ip_class}
Address Type        : {address_type}

NETWORK PROPERTIES

Private Address     : {'Yes' if address_type == 'Private' else 'No'}
Public Address      : {'Yes' if address_type == 'Public' else 'No'}
Loopback Address    : {'Yes' if ip.is_loopback else 'No'}
Link-Local Address  : {'Yes' if ip.is_link_local else 'No'}
Multicast Address   : {'Yes' if ip.is_multicast else 'No'}
Reserved Address    : {'Yes' if ip.is_reserved else 'No'}
Unspecified Address : {'Yes' if ip.is_unspecified else 'No'}
Globally Reachable  : {'Yes' if ip.is_global else 'No'}

ADDRESS REPRESENTATION

Binary Address      : {binary}
Integer Value       : {int(ip)}

=============================================
IP ADDRESS ANALYSIS COMPLETED.
"""

            self.write_output(self.info_output, result)

        except Exception as error:

            self.write_output(
                self.info_output,
                f"ERROR: {error}"
            )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = NetScope(root)

    root.mainloop()
