CalcOS

Author: Odafeigho

CalcOS is a cross-platform scientific calculator built with Python and Kivy, inspired by advanced Casio calculators like the ClassWiz CW Series. It features a modular, intuitive user interface with high-contrast labels, simulation functions, and graphical solutions, designed for approachability and familiarity. The app runs on desktop and mobile platforms, providing a responsive layout for students, educators, and professionals.

Features





Calculator Tab:





Numeric and scientific functions in a single, Casio-inspired keypad layout.



Supports basic arithmetic (+, -, *, /, %, ^), trigonometric functions (sin, cos, tan, arcsin, arccos, arctan), logarithms (log, ln), and more (sqrt, abs, fact, pi, e).



Simulation functions: dice (random 1-6) and coin (random Heads/Tails) for interactive learning.



High-contrast UI with a red "C" (Clear) button for intuitive operation.



Graphing Tab:





Plot mathematical functions (e.g., sin(x), x**2) over the x-range [-10, 10].



Input field for expressions and a "Plot" button for visualization.



Displays graphs with grid, labels, and legend, mimicking Casio's clear graphing style.



Error handling for invalid expressions.



History Tab:





Placeholder for future implementation to store and display past calculations.



Responsive Design:





Cross-platform compatibility (Windows, macOS, Linux, iOS, Android).



Modular UI with a tabbed interface for easy navigation.



Planned Features:





QR code integration for sharing graphs via ClassPad.net (requires additional libraries).



History tab functionality for calculation logging.



Advanced graphing features like zoom/pan controls and multiple graph plotting.

Installation

Prerequisites





Python 3.6 or higher



Internet connection (for initial dependency installation)



Administrative privileges (may be required for dependency installation)

Steps





Clone or Download the Repository:

git clone <repository-url>
cd calcos

Alternatively, download the calcos.py file directly.



Install Dependencies: The app automatically checks for and installs required dependencies (setuptools, kivy, matplotlib) using pip. Run the app to trigger this process:

python calcos.py

If you encounter permission errors, try:

sudo python calcos.py  # Linux/macOS

or run as administrator on Windows.



Manual Dependency Installation (optional): If the automatic installation fails, manually install the dependencies:

pip install setuptools kivy matplotlib



Run the App:

python calcos.py

Usage





Launch the App: Run python calcos.py to open the CalcOS interface, which starts on the Calculator tab.



Calculator Tab:





Use the keypad to input numbers, operators, and scientific functions.



Example: Enter sin(0.5) and press = to compute the result.



Use dice or coin buttons for random simulations.



Press C to clear the display.



Graphing Tab:





Navigate to the Graph tab.



Enter a mathematical expression (e.g., x**2, sin(x), cos(x) + 1) in the input field.



Press the "Plot" button to display the graph over x = [-10, 10].



Invalid expressions will display an error message.



History Tab:





Currently a placeholder, displaying "Calculation history will appear here."

Project Structure





calcos.py: The main application file containing all logic and UI components.





Modules:





ScientificCalculator: Backend logic for calculations and simulations.



Display: Read-only text input for showing expressions and results.



Keypad: 6-column grid with numeric, scientific, and simulation buttons.



HistoryPanel: Placeholder for calculation history.



GraphingPanel: UI for plotting mathematical functions using Matplotlib.



CalcOSApp: Main tabbed interface integrating all modules.

Dependencies





setuptools: For package management (pkg_resources).



kivy: For the cross-platform UI.



matplotlib: For graphing mathematical functions.



numpy: For generating x-values in graphs.

These are automatically installed when running the app, or you can install them manually with pip.

Notes





Permissions: Dependency installation may require administrative privileges. Use sudo or run as administrator if prompted.



Internet Connection: Required for initial dependency installation.



Limitations:





The History tab is a placeholder and does not yet store calculations.



QR code integration for graph sharing is planned but not implemented (requires the qrcode library).



Future Enhancements:





Implement the History tab to log calculations.



Add zoom/pan controls for graphs.



Support multiple graph plotting.



Integrate QR code generation for sharing graphs with external tools like ClassPad.net.

Contributing

Contributions are welcome! To contribute:





Fork the repository.



Create a feature branch (git checkout -b feature-name).



Commit your changes (git commit -m 'Add feature').



Push to the branch (git push origin feature-name).



Open a pull request.

Please ensure code follows the existing style and includes tests for new features.

License

This project is licensed under the MIT License. See the LICENSE file for details (to be added).

Acknowledgments





Inspired by the Casio ClassWiz CW Series calculators, known for their approachability and award-winning design.



Built with Kivy for cross-platform UI and Matplotlib for graphing.
