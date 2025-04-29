ECE 2774 - Advanced Power Systems Analysis
Project 3 - Power System Simulator Enhancement
Cecilia Espadas

Purpose and Theoretical Background

The scope of this enhancement focuses on the integration of synchronous condensers into a power system simulation framework. This addition addresses a critical need in modern power systems, especially as they incorporate more renewable energy sources and face challenges with grid stability. By introducing synchronous condensers, this update enables users to simulate voltage regulation and reactive power compensation in systems that have weak voltage profiles or long transmission distances. These devices play a key role in stabilizing voltage, particularly when traditional generators are not available to provide dynamic reactive power support. Synchronous condensers don’t generate real power, they regulate voltage by injecting or absorbing reactive power. Synchronous condensers help stabilize the system by maintaining voltage near a setpoint similar to a PV bus with some major differences. In this implementation, the simulator models synchronous condensers as PV-type components that try to hold their voltage magnitude constant by adjusting reactive power. Real power losses are assumed to be small and are approximated as 2% of the unit’s MVAR rating. The simulator subtracts this from the power balance during power flow.

If a synchronous condenser hits its reactive limit (either q_max or q_min), it can’t maintain its voltage anymore. When that happens, it automatically switches from a PV bus to a PQ bus, and voltage is no longer fixed and it becomes a variable in the Newton-Raphson solver. The simulator updates this during iterations and includes the ΔQ mismatch to reflect the change. Adding this functionality makes the simulator more realistic and lets users study how voltage control works in transmission systems with synchronous condensers, including how the limits affect system behavior during power flow.

From a theoretical standpoint, a synchronous condenser behaves similarly to a generator in steady-state analysis, contributing to the voltage magnitude at its connected bus and influencing reactive power flows. Synchronous condensers differ from generators in two critical ways: They do not supply active power (aside from small real power losses) and their reactive output is typically limited by operational bounds, requiring enforcement logic when simulating.

The new SynchronousCondenser module integrates seamlessly with the existing power system simulator by acting as an additional component within the circuit. It is added with the add_sync_condenser method, which connects the condenser to a bus and defines its maximum reactive power limit. The module interacts with the existing power flow calculation in the Solution class, adjusting its reactive power output to regulate voltage at its connected bus. If the reactive power limit is reached, the condenser automatically switches from a PV bus to a PQ bus. This enhancement enhances the simulator’s ability to model reactive power compensation and voltage regulation in real-world power systems, while maintaining modularity and clean integration with the core simulator framework.


Inputs and Outputs

To add the synchronous condenser to the circuit, the method add_sync_condenser is used. The method takes 3 inputs:
      The name of the synchronous condenser, as a string
      The bus that the synchronous condenser is connected to, as a string
      The maximum reactive power output for the synchronous condenser, q_max, in MVAR, as a float

An example of how to add a synchronous condenser to the circuit is below:
      circuit1.add_sync_condenser("SC1", "Bus9", 250)
      
When the synchronous condenser is added, the following attributes/factors are updated:
      circuit.syncons: the dictionary of SynchronousCondenser objects
      bus.bus_type: automatically set to "PV Bus" upon addition
      power_mismatch(): uses the enforce_q_limits() method to clamp output and apply penalties to ΔQ if the voltage can no longer be controlled
      The per-unit contributions to ΔP include a real power loss of 2% of q_max.

When the power_flow method is run, the outputs are as follows:
      The maximum power mismatch for each iteration of the Newton-Raphson algorithm
      The number of iterations it took for the algorithm to run
      The final angle for each bus in radians
      The final voltage for each bus in per units
      The final power mismatch
      The final Jacobian matrix


How to Test

To test the power system simulator, follow the steps below. These instructions apply to both test cases provided and ensure the system is functioning correctly, including verifying voltage regulation and reactive power compensation by the synchronous condensers.
      Install numpy and pandas if you have not already
      Run the Example 1 script (Main_1SynCon.py) to test a system with one synchronous condenser at Bus9:
            Expected: System converges, Bus9 voltage stays close to 1.0 p.u., power mismatch near zero, condenser does not exceed 250 MVAR.
      Run theExample 2 script (Main_2SynCon.py) to test a system with two synchronous condensers at Bus9 and Bus10:
            Expected: System converges, Bus9 and Bus10 voltages stay close to 1.0 p.u., power mismatch near zero, condensers stay within their limits (250 MVAR and 100 MVAR).
      After running, check that:
            All buses have voltages near their expected values.
            No synchronous condenser exceeds its reactive power limits.
            System converges in a few iterations with small final mismatch values.


Example Test Scenarios

The testing strategy for this simulator enhancement focuses on validating that the synchronous condensers regulate bus voltage properly under normal power flow conditions. Two example test cases were created: one with a single synchronous condenser and one with two synchronous condensers. Testing checked that the system converged correctly, bus voltages remained stable, and reactive power outputs stayed within specified limits. Testing did not focus on forcing the condensers to reach their reactive power limits, but future enhancements could expand on limit enforcement scenarios. The full detailed description for these test cases, the example code, and full expected output/print out can be seen in the "Project 3 Documentation" PDF.

Example 1: Standard Power Flow Test (Normal Operation)
Objective: The goal of this test is to verify that the synchronous condenser regulates voltage properly under typical power flow conditions in a given system. The system is set up with several buses, transmission lines, transformers, generators, and loads. The test will check if the synchronous condenser correctly contributes to voltage regulation by adjusting reactive power output and maintaining the voltage within the desired limits.

Test Setup: To test the power system simulator in Python, you can create a test circuit using the components defined in the simulator, such as buses, transmission lines, transformers, generators, loads, and the synchronous condenser. The components used in this first example are below:

Bus1: Slack Bus (20 kV)
Bus2–Bus6: PQ Buses (230 kV)
Bus7: PV Bus (18 kV)
Bus9: PV Bus (20kV)
      This bus is treated as a PV bus because it has a synchronous condenser connected to it.
Transmission Lines:
      6 lines using "Partridge" conductor, 2-conductor bundle, and fixed geometry
      Lengths range from 10 to 35 miles
Transformers:
      T1: Connects Bus1 to Bus2, 125 MVA, delta-Y grounded, 1 Ω grounding
      T2: Connects Bus6 to Bus7, 200 MVA, delta-Y grounded, 999999 Ω grounding
      T3: Connects Bus8 to Bus9, 125 MVA, delta-Y grounded, 1 Ω grounding
Generators:
      G1 at Bus1: 20 MW, 100 MVAR
      G2 at Bus7: 18 MW, 200 MVAR
Loads:
      L1 at Bus3: 110 MW, 50 MVAR
      L2 at Bus4: 100 MW, 70 MVAR
      L3 at Bus5: 100 MW, 65 MVAR
Synchronous Condenser:
      SC1 at Bus 9: 250 MVAR

After setting up the circuit, you initialize the Solution object, which runs the power flow calculation and simulates the system’s behavior. Once the simulation is complete, you can analyze the output, such as voltage values, power mismatch, and reactive power adjustment, to verify that the system behaves as expected. 

Expected Output: The results for this code will show that the system converged in 4 iterations with the maximum mismatch reducing from 2.0 to 0.0000, indicating successful convergence. The voltage at Bus9, where the synchronous condenser is connected, remained stable at 1.0 per unit, confirming effective voltage regulation. The power mismatch values are near zero, indicating a balanced system. The Jacobian matrix reflects the expected sensitivity to voltage and angle adjustments, showing that the synchronous condenser is contributing appropriately to voltage control at Bus9. These results confirm that the simulation is functioning as intended,

Example 2: Reactive Power Compensation with Multiple Synchronous Condensers
Objective: The goal of this test is to assess the system's ability to manage multiple synchronous condensers across different buses and verify if they can collectively regulate voltage and provide necessary reactive power support. The test will simulate a system with two synchronous condensers, one connected to Bus9 and the other to Bus10, and check if their reactive power outputs stay within limits and contribute to overall system stability.

Test Setup: To test the power system simulator in Python, you can create a test circuit using the components defined in the simulator, such as buses, transmission lines, transformers, generators, loads, and synchronous condensers. The components used in the second example are below:

Bus1: Slack Bus (20 kV)
Bus2–Bus6: PQ Buses (230 kV)
Bus7: PV Bus (18 kV)
Bus9: PV Bus (20kV)
      This bus is treated as a PV bus because it has a synchronous condenser connected to it.
Bus10: PV Bus (20kV)
      This bus is treated as a PV bus because it has a synchronous condenser connected to it.
Transmission Lines:
      6 lines using "Partridge" conductor, 2-conductor bundle, and fixed geometry
      Lengths range from 10 to 35 miles
Transformers:
      T1: Connects Bus1 to Bus2, 125 MVA, delta-Y grounded, 1 Ω grounding
      T2: Connects Bus6 to Bus7, 200 MVA, delta-Y grounded, 999999 Ω grounding
      T3: Connects Bus8 to Bus9, 125 MVA, delta-Y grounded, 1 Ω grounding
      T4: Connects Bus6 to Bus10, 125 MVA, delta-Y grounded, 1 Ω grounding
Generators:
      G1 at Bus1: 20 MW, 100 MVAR
      G2 at Bus7: 18 MW, 200 MVAR
Loads:
      L1 at Bus3: 110 MW, 50 MVAR
      L2 at Bus4: 100 MW, 70 MVAR
      L3 at Bus5: 100 MW, 65 MVAR
Synchronous Condenser:
      SC1 at Bus 9: 250 MVAR
      SC2 at Bus 10: 100 MVAR
      
After setting up the circuit, you initialize the Solution object, which runs the power flow calculation and simulates the system’s behavior with multiple synchronous condensers. Once the simulation is complete, you can analyze the output, such as the voltage values at each bus, the reactive power outputs of the condensers, and the power mismatch to ensure the system is stable and voltage regulation is maintained. In this second example, the focus is on verifying the interaction between two synchronous condensers at Bus9 and Bus10, ensuring they both regulate voltage and operate within their specified reactive power limits.

Expected Output: The results from this example will indicate that the system has successfully converged in 3 iterations, with the maximum mismatch decreasing from 2.0 to 0.0000, which is a clear sign of convergence and indicates that the power flow solution is stable. The final bus voltages show that all buses, including Bus9 and Bus10 (where the synchronous condensers are connected), have reached stable voltage values of 1.0 per unit, confirming that the synchronous condensers are regulating the voltage properly. The power mismatch values are near zero for all buses, which suggests the system is balanced, and there are no significant discrepancies between injected and consumed power. The Jacobian matrix reflects the sensitivities of the system, showing the interaction between buses, and the results confirm that the synchronous condensers are appropriately contributing to reactive power compensation.


Typical Use Cases and Failure Modes

The typical use cases for this simulator involve running power flow simulations where the main goal is to maintain system stability. In these cases the synchronous condensers regulate voltage by adjusting their reactive power output. These devices are useful in systems with weak voltage profiles, helping to keep the voltage at specific buses within desired limits. Under normal operating conditions, the synchronous condenser will regulate voltage as expected, providing critical reactive power support while staying within its operational limits. The simulation tracks these adjustments and ensures that voltage regulation remains consistent.

Edge cases were tested by observing the system behavior when multiple synchronous condensers were added to the network under realistic loading conditions. Testing confirmed that the condensers regulated bus voltage without exceeding their reactive power limits and that the simulator maintained stable convergence even with additional reactive support devices connected. Extreme limit behavior was not directly tested in these examples but could be added as a future enhancement.

This simulator does not currently include synchronous condensers in fault analysis. While synchronous condensers play a key role in voltage regulation under normal conditions, their behavior during faults—such as voltage dips, short circuits, or system disturbances—is not modeled in the current framework. The omission of synchronous condensers from fault simulations limits the ability to fully understand how these devices interact with the grid during fault conditions, particularly in weak grid scenarios where their reactive power capabilities could significantly influence recovery and stability. This could be a potential area for future enhancements in the simulator.

The simulator is designed to handle common issues that might arise during power flow simulations, such as when a synchronous condenser reaches its reactive power limits. But, there are failure modes that have not been addressed. If the system fails to switch a synchronous condenser from a PV bus to a PQ bus once its reactive power limits are hit, the simulation would not currently provide an error message or take corrective action. If the condenser exceeds its operational bounds, the simulation does not yet enforce a hard limit on the reactive power, which could lead to inaccurate voltage control or power flow results. These potential failures show the areas that need improvement and where better error handling and system checks could be implemented.


How the Code was Validated

The validation process for this enhancement was done by using PowerWorld, based on the 7-bus system from Project 2. To update the system for the synchronous condenser, two additional buses, one additional transmission line, and one additional transformer were added. Previously tested and validated numbers were used for these components to ensure they were correct. Once these updates were made, the synchronous condenser could be added into the system.

With the PowerWorld system set up, the first step of validation was ensuring the Ybus was correct. Since the synchronous condenser does not affect the Ybus, validating this first ensured that the simulator was still calculating the Ybus correctly with the additional transmission lines and transformers. After confirming the Ybus was correct, the next step was validating the initial power mismatches from a flat start. Because the synchronous condenser injects reactive power and absorbs approximately 2% of its rated reactive power in real power losses, the expected power mismatches needed to be updated accordingly. Once the adjustment was made, the initial power mismatch values from the Python code were directly compared to the values from PowerWorld, both reset to a flat start. These matched exactly.

After validating the initial mismatches, the next step was checking the initial Jacobian from a flat start. The Jacobian matrix calculated in the Python code matched PowerWorld’s Jacobian, verified by calculating the percent differences across all entries. Once the values at the flat start were validated, the final bus voltages were compared after running Newton-Raphson in both PowerWorld and the Python simulator. Again, percent differences were used to compare, and the results matched closely.
Finally, the final Jacobian matrix after Newton-Raphson convergence was validated. The maximum percent difference between the Python code and PowerWorld for the final Jacobian was 1.00%, which is likely due to rounding differences within PowerWorld. With all stages of validation complete — Ybus, initial mismatches, initial Jacobian, final voltages, and final Jacobian — it was confirmed that the Python simulator accurately modeled the system’s behavior, including the behavior of the synchronous condensers. The synchronous condenser model used in PowerWorld was based on standard equipment ratings, academic references, and guidance from the course instructors, ensuring the overall validation was consistent with realistic system behavior. To view the validation process, please see the excel file titled “Project 3 Validation” on my GitHub repository.

While validating the final bus angles, larger percent differences were observed between the Python simulator and PowerWorld, with some differences reaching up to 389%. This is expected because voltage angles are small numbers in radians, and even tiny absolute differences can cause large percent differences. Despite the differences in angles, the system still converges properly, the final bus voltages match closely, and the power mismatches are near zero. Because of this, the differences in final bus angles are considered acceptable and do not impact the overall validity of the simulation results.


References

J. D. Glover, T. J. Overbye, and M. S. Sarma, Power System Analysis and Design, 6th ed., Cengage Learning, 2012.

P. A. Boheme, “Simulation of Power System Response to Reactive Power Compensation,” TRACE: Tennessee Research and Creative Exchange, Aug. 2006. [Online]. Available: https://trace.tennessee.edu/cgi/viewcontent.cgi?article=2951&context=utk_gradthes. [Accessed: Apr. 24, 2025].

“Synchronous condensers,” ENTSO-E. [Online]. Available: https://www.entsoe.eu/technopedia/techsheets/synchronous-condenser/. [Accessed: Apr. 24, 2025].

“Synchronous condensers enhancing grid stability,” Siemens Energy. [Online]. Available: https://www.siemens-energy.com/us/en/home/stories/grid-stability-north-america.html. [Accessed: Apr. 24, 2025].

“Synchronous condensers technical data,” Motors and Generators. [Online]. Available: https://new.abb.com/motors-generators/synchronous-condensers/technical-data. [Accessed: Apr. 24, 2025].
