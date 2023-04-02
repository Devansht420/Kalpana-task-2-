import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QTimer, QDateTime
 
 
class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()
 
        # Set the size of the window and the title
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Live Graph")
 
        # Create a QWidget to hold the plot and telemetry data
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
 
        # Create a vertical layout for the plot and telemetry data
        self.layout = QVBoxLayout(self.central_widget)
 
        # Create a label for displaying telemetry data
        self.telemetry_label = QLabel(self.central_widget)
        self.layout.addWidget(self.telemetry_label)
 
        # Create a Matplotlib figure and axis for the plot
        self.figure = plt.figure()
        self.axis = self.figure.add_subplot(111)
 
        # Create a Matplotlib canvas widget to display the plot
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
 
        # Set the plot title and labels
        self.axis.set_title("Altitude vs Time")
        self.axis.set_xlabel("Time (s)")
        self.axis.set_ylabel("Altitude (m)")
 
        # Set up the CSV file and the data arrays
        self.csv_file = "telemetry.csv"
        self.time_data = []
        self.altitude_data = []
 
        # Set up a QTimer to update the plot and telemetry data at a rate of 1 package/sec
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)
 
        # Set up a QTimer to update the plot at a rate of 30 frames/sec
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plot)
        self.plot_timer.start(33)
 
        # Schedule the next update time
        self.next_update_time = QDateTime.currentDateTime().addSecs(1)
 
        # Start the GUI
        self.show()
 
    def update_data(self):
        # Read the latest row of data from the CSV file
        df = pd.read_csv(self.csv_file)
        latest_row = df.iloc[-1]
        team_id_value = latest_row["TEAM_ID"]
        mission_time_value = latest_row["MISSION_TIME"]
        packet_count_value = latest_row["PACKET_COUNT"]
        packet_type_value = latest_row["PACKET_TYPE"]
        mode_value = latest_row["MODE"]
        payload_released_value = latest_row["PAYLOAD_RELEASED"]
        altitude_value = float(latest_row["ALTITUDE"])
        temperature_value = float(latest_row["TEMP"])
        voltage_value = float(latest_row["VOLTAGE"])
         
        # Add the new data to the data arrays
        self.altitude_data.append(altitude_value)
         
        # Update the telemetry label with the latest data
        telemetry_text = f"Team ID: {team_id_value}\nMission Time: {mission_time_value}\nPacket Count: {packet_count_value}\nPacket Type: {packet_type_value}\nMode: {mode_value}\nPayload Released: {payload_released_value}\nAltitude: {altitude_value:.2f} m\nTemperature: {temperature_value:.2f} C\nVoltage: {voltage_value:.2f} V\nNext update: {self.next_update_time.toString('hh:mm:ss')}"
        self.telemetry_label.setText(telemetry_text)
 
        # Schedule the next update time
        self.next_update_time = QDateTime.currentDateTime().addSecs(1)
 
    def update_plot(self):
        # Plot the data on the graph
        self.axis.clear()
        self.axis.plot(self.time_data, self.altitude_data, 'r-')
        self.canvas.draw()
 
 
if __name__ == "__main__":
    # Create the QApplication
    app = QApplication(sys.argv)
 
    # Create the graph window
    window = GraphWindow()
 
    # Update the live graph
    while True:
        app.processEvents()
 