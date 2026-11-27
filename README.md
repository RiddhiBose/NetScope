<div align="center">

# NetScope

**Interactive Network Utility Dashboard**

A single-file, browser-based toolkit for subnetting, VLSM planning, binary conversion, connectivity checks and IP lookups, with a built-in command terminal.

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Version](https://img.shields.io/badge/version-1.0-0ea5e9?style=flat-square)
![Platform](https://img.shields.io/badge/platform-web%20browser-334155?style=flat-square)
![Dependencies](https://img.shields.io/badge/dependencies-none-22c55e?style=flat-square)

</div>

---

## Overview

NetScope brings the networking calculations students and engineers use most into one dark-themed dashboard. No installation, no frameworks, no build step. Open the file in a browser and start working.

Every tool can be used through the graphical panels or through the integrated command terminal.

> **Scope:** NetScope is an educational and utility tool. It is not an enterprise monitoring system, packet analyzer, or security assessment platform.

---

## Tools

| Tool | What it does |
|---|---|
| **Subnet Calculator** | Network ID, broadcast address, subnet mask, wildcard mask, first/last usable IP and usable host count from an IPv4 address and CIDR prefix |
| **Binary Converter** | Converts IPv4 addresses into 8-bit-per-octet binary to show the 32-bit structure |
| **VLSM Calculator** | Allocates variable-length subnets from a parent network based on per-department host requirements |
| **Network Diagnostics** | Browser-based connectivity check with request status and response timing |
| **IP Information Lookup** | Fetches ISP, organization, location and timezone data from an external IP information service |
| **Command Terminal** | Opens and runs tools through short text commands |

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/RiddhiBose/NetScope.git
cd NetScope

# Open in your browser
# Windows:  start index.html
# macOS:    open index.html
# Linux:    xdg-open index.html
```

You can also just double-click the HTML file. No server required.

> If your main file has a different name, replace `index.html` above.

---

## Examples

### Subnet Calculator

**Input:** `192.168.1.10/24`

| Parameter | Result |
|---|---|
| Subnet Mask | `255.255.255.0` |
| Wildcard Mask | `0.0.0.255` |
| Network ID | `192.168.1.0` |
| Broadcast ID | `192.168.1.255` |
| First Usable IP | `192.168.1.1` |
| Last Usable IP | `192.168.1.254` |
| Total Addresses | `256` |
| Usable Hosts | `254` |

### Binary Converter

```
192.168.1.10
11000000.10101000.00000001.00001010
```

### VLSM Allocation

**Parent network:** `192.168.1.0/24`

| Department | Hosts Needed | Allocated Subnet | Mask | Usable Hosts |
|---|---|---|---|---|
| Administration | 100 | `192.168.1.0/25` | `255.255.255.128` | 126 |
| IT Department | 50 | `192.168.1.128/26` | `255.255.255.192` | 62 |
| HR Department | 25 | `192.168.1.192/27` | `255.255.255.224` | 30 |
| Finance | 10 | `192.168.1.224/28` | `255.255.255.240` | 14 |

240 of 256 addresses allocated, 16 remaining.

The allocator sorts requirements from largest to smallest, assigns the smallest prefix that fits each one, and checks that nothing overlaps or exceeds the parent network.

---

## Command Terminal

```
netscope> help
```

| Command | Action |
|---|---|
| `help` | List available commands |
| `subnet` | Open the Subnet Calculator |
| `binary` | Open the Binary Converter |
| `vlsm` | Open the VLSM Calculator |
| `diag` | Open Network Diagnostics |
| `lookup` | Open IP Information Lookup |
| `clear` | Clear terminal output |

Unrecognized commands return guidance instead of failing silently.

---

## Architecture

```
  User Input
      |
      v
  Input Validation
      |
      v
  Processing  ---------->  Network Request (diagnostics, IP lookup)
      |                            |
      v                            v
  Result Generation  <-------------+
      |
      v
  Dashboard Output
```

| Layer | Responsibility |
|---|---|
| **User Interface** | Sidebar, cards, input fields, buttons, output panels |
| **Application Logic** | Validation, subnet math, binary conversion, VLSM allocation |
| **Network Request** | Browser-based connectivity checks and external IP lookups |
| **Terminal Interface** | Command parsing and tool navigation |

Everything (markup, styles, scripts) lives in a single HTML file, so the project is trivial to share, host, and read.

---

## Testing

| Module | Test | Expected Outcome |
|---|---|---|
| Subnet Calculator | Valid IPv4 and prefix | Subnet details displayed |
| Subnet Calculator | Invalid IP | Validation message |
| Binary Converter | Valid IPv4 | Binary representation generated |
| VLSM Calculator | Valid parent network and requirements | Non-overlapping subnets allocated |
| VLSM Calculator | Requirements exceed capacity | Allocation error displayed |
| Network Diagnostics | Supported target URL | Status and timing, subject to browser limits |
| IP Lookup | Supported IP address | Data returned if the external service is reachable |
| Terminal | Supported command | Matching tool opens |
| Terminal | Unsupported command | Guidance message |

---

## Limitations

- IPv4 only. IPv6 subnet calculations are not yet supported.
- Network Diagnostics uses HTTP-based browser requests, not ICMP ping, so timings differ from command-line tools.
- CORS and other browser security policies can block requests to some targets.
- IP lookup depends on an external service; data may be incomplete, outdated, or approximate. IP geolocation is never an exact physical location.
- No packet capture, traffic analysis, or continuous monitoring.

---

## Roadmap

- [ ] IPv6 support
- [ ] Export results (subnet and VLSM tables)
- [ ] Network topology visualization
- [ ] Expanded terminal commands and shortcuts
- [ ] Additional connectivity and response analysis tools
- [ ] Optional network monitoring through external services
- [ ] More dashboard visualizations

---

## Tech Stack

| Technology | Purpose |
|---|---|
| HTML | Structure |
| CSS | Styling, layout, dark theme |
| JavaScript | Calculations, validation, interactions, terminal |
| Browser Networking APIs | Connectivity checks |
| External IP information service | IP lookup data |

---

## Project Information

| | |
|---|---|
| **Project** | NetScope v1.0 |
| **Type** | Web-based networking utility toolkit |
| **Author** | Riddhi Bose |
| **Roll Number** | 2500320310098 |
| **Department** | Electronics and Communication Engineering |
| **Institution** | ABES Engineering College |
| **Academic Year** | 2026 |

---

## References

- [MDN: HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [MDN: CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [MDN: JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- IPv4 addressing, CIDR, and VLSM concepts
- Browser networking, HTTP requests, and CORS documentation

---

<div align="center">

Built with HTML, CSS, and JavaScript by [Riddhi Bose](https://github.com/RiddhiBose)

</div>
