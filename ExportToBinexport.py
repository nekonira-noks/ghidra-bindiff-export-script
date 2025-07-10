# -*- coding: utf-8 -*-
# Ghidra Python Script: ExportToBinexport_Step4.py
#
# @category UserScript
# @toolbar
#
# Step 4: Search for BinExport exporter

import os
from ghidra.app.util.exporter import ExporterLocator # Import to find Exporters
from ghidra.util.task import ConsoleTaskMonitor     # Import for task monitor

# Standard functions and variables available in Ghidra scripts
# getCurrentProgram(): Function to get the currently opened program object in Ghidra
# getScriptArgs(): Function to get script arguments passed in headless mode
# println(): Function to output messages to the console
# printerr(): Function to output error messages to the console

def run():
    println("Step 4: Script started.")

    # 1. Get script arguments
    args = getScriptArgs()
    if len(args) < 2:
        printerr("Error: Not enough arguments. At least two arguments are required.")
        printerr("Usage: <script_name>.py <output_base_directory> <firmware_model>")
        return

    output_base_dir_arg = args[0]
    firmware_model_arg = args[1]

    println("Received output base directory: " + output_base_dir_arg)
    println("Received firmware model: " + firmware_model_arg)

    # 2. Get the current program
    program = getCurrentProgram()
    if program is None:
        printerr("Error: No program is currently open.")
        return
    program_name = program.getName()
    println("Currently processing program name: " + program_name)

    # 3. Construct and create the output directory
    firmware_specific_output_dir = os.path.join(output_base_dir_arg, firmware_model_arg)
    println("Constructed output directory path: " + firmware_specific_output_dir)
    try:
        if not os.path.exists(firmware_specific_output_dir):
            os.makedirs(firmware_specific_output_dir)
            println("Directory created: " + firmware_specific_output_dir)
        else:
            println("Directory already exists: " + firmware_specific_output_dir)
    except OSError as e:
        printerr("Error: Failed to create directory. Path: {}, Error: {}".format(firmware_specific_output_dir, e))
        return

    # 4. Search for BinExport exporter --- (New part starts here) ---
    monitor = ConsoleTaskMonitor() # Create a task monitor for headless mode
    exporter_to_use = None       # Variable to store the found exporter

    println("Searching for available exporters...")
    try:
        # Get all exporters available for the current program
        exporters = ExporterLocator.getExporters(program, monitor)
    except Exception as e: # Also catch Java exceptions, etc.
        printerr("Error: Exception occurred during ExporterLocator.getExporters call: " + str(e))
        # import traceback
        # printerr(traceback.format_exc()) # Uncomment for detailed stack trace if needed
        return

    println("--- List of available exporters ---")
    for exporter_candidate in exporters:
        println(" - " + exporter_candidate.getName()) # Display the name of each exporter
        # The name of the BinExport exporter is "BinExport" or "BinExport (Experimental)", etc.
        # Check if "binexport" (case-insensitive) is included in the name.
        if "binexport" in exporter_candidate.getName().lower():
            exporter_to_use = exporter_candidate
            # Use the first exporter found that contains "binexport".
            # Usually, there should be only one.
            break # Exit the loop when BinExport exporter is found
    println("-----------------------------")

    if exporter_to_use is None:
        printerr("Error: BinExport exporter was not found.")
        printerr("Please check that the BinExport extension is properly installed and enabled in Ghidra.")
        # You may abort here, but for now, continue to the end (return is commented out)
        # return
    else:
        println("Exporter to use found: " + exporter_to_use.getName())
    # --- (New part ends here) ---

    println("Step 4: Exporter search process completed.")

if __name__ == "__main__":
    run()