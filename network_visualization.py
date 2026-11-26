
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(10, 6))

# Department boxes
dev = patches.Rectangle(
    (0.5, 2), 4, 2,
    linewidth=2, edgecolor="blue",
    facecolor="lightblue"
)

finance = patches.Rectangle(
    (5.5, 2), 4, 2,
    linewidth=2, edgecolor="green",
    facecolor="lightgreen"
)

ax.add_patch(dev)
ax.add_patch(finance)

# Development department
ax.text(2.5, 3.6, "DEVELOPMENT TEAM",
        ha="center", fontsize=12, weight="bold")

ax.text(2.5, 3, "192.168.1.0/25",
        ha="center", fontsize=11)

ax.text(2.5, 2.5, "Dev-PC1     Dev-PC2",
        ha="center", fontsize=10)

# Finance department
ax.text(7.5, 3.6, "FINANCE / HR TEAM",
        ha="center", fontsize=12, weight="bold")

ax.text(7.5, 3, "192.168.1.128/25",
        ha="center", fontsize=11)

ax.text(7.5, 2.5, "Finance-PC1     HR-PC1",
        ha="center", fontsize=10)

# Security boundary
ax.plot([5, 5], [1.5, 4.5], "r--", linewidth=2)

ax.text(5, 1.1, "SECURITY BOUNDARY",
        ha="center", color="red", fontsize=10)

ax.set_title("SECURE STARTUP LAN TOPOLOGY",
             fontsize=15, weight="bold")

ax.set_xlim(0, 10)
ax.set_ylim(0.5, 5)
ax.axis("off")

plt.savefig("network_topology.png", dpi=300)
plt.show()
