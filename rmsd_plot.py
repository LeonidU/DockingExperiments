import matplotlib.pyplot as plt

# Parse the xvg file and extract data
time = []
rmsd = []

with open('rmsd.xvg') as f:
    for line in f:
        if not line.startswith(('@', '#')):
            values = line.split()
            time.append(float(values[0]))  # Time (ns)
            rmsd.append(float(values[1]))  # RMSD (nm)

# Plot the data
plt.plot(time, rmsd, label='RMSD over time')
plt.xlabel('Time (ns)')
plt.ylabel('RMSD (nm)')
plt.title('RMSD vs Time for Protein')
plt.legend()

# Save the plot to a PNG file
plt.savefig('rmsd_plot.png', dpi=300)

# Optionally, display the plot
# plt.show()
