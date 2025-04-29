# Cece Espadas - Project 3
# ECE 2774
# Synchronous Condenser

from Circuit import Circuit
from Solution import Solution

# create test circuit
circuit2 = Circuit("Test Circuit")

# ADD BUSES
circuit2.add_bus("Bus1", 20)
circuit2.add_bus("Bus2", 230)
circuit2.add_bus("Bus3", 230)
circuit2.add_bus("Bus4", 230)
circuit2.add_bus("Bus5", 230)
circuit2.add_bus("Bus6", 230)
circuit2.add_bus("Bus7", 18)
circuit2.add_bus("Bus8", 230)
circuit2.add_bus("Bus9", 20)
circuit2.add_bus("Bus10", 20)

# ADD TRANSMISSION LINES
circuit2.add_conductor("Partridge", 0.642, 0.0217, 0.385, 460)
circuit2.add_bundle("Bundle1", 2, 1.5, "Partridge")
circuit2.add_geometry("Geometry1", 0, 0, 18.5, 0, 37, 0)

circuit2.add_tline("Line1", "Bus2", "Bus4", "Bundle1", "Geometry1", 10)
circuit2.add_tline("Line2", "Bus2", "Bus3", "Bundle1", "Geometry1", 25)
circuit2.add_tline("Line3", "Bus3", "Bus5", "Bundle1", "Geometry1", 20)
circuit2.add_tline("Line4", "Bus4", "Bus6", "Bundle1", "Geometry1", 20)
circuit2.add_tline("Line5", "Bus5", "Bus6", "Bundle1", "Geometry1", 10)
circuit2.add_tline("Line6", "Bus4", "Bus5", "Bundle1", "Geometry1", 35)
circuit2.add_tline("Line7", "Bus3", "Bus8", "Bundle1", "Geometry1", 10)

# ADD TRANSMORMERS
circuit2.add_transformer("T1", "Bus1", "Bus2", 125, 8.5, 10, "delta-y", 1)
circuit2.add_transformer("T2", "Bus6", "Bus7", 200, 10.5, 12, "delta-y", 999999)
circuit2.add_transformer("T3", "Bus8", "Bus9", 125, 8.5, 10, "delta-y", 1)
circuit2.add_transformer("T4", "Bus6", "Bus10", 125, 8.5, 10, "delta-y", 1)

# ADD GENERATORS
circuit2.add_generator("G1", "Bus1", 20, 100, 0, True)
circuit2.add_generator("G2", "Bus7", 18, 200, 1, True)

# ADD LOAD
circuit2.add_load("L1", "Bus3", 110, 50)
circuit2.add_load("L2", "Bus4", 100, 70)
circuit2.add_load("L3", "Bus5", 100, 65)

# ADD SYNCHRONOUS CONDENSER
circuit2.add_sync_condenser("SC1", "Bus9", 250)
circuit2.add_sync_condenser("SC2", "Bus10", 100)

solution = Solution(circuit2)

solution.power_flow()
