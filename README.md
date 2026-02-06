# Kapitan Language Server

A Visual Studio Code extension for [Kapitan](https://github.com/kapicorp/kapitan), providing language server features to improve your development workflow.

## Features

*   **Go to Definition**: Quickly navigate to the definition of Kapitan classes within your inventory.

## Requirements

This extension requires **Python 3.12** or newer to be installed on your system.

*   The extension utilizes a Python-based language server.
*   Upon installation/startup, the extension will attempt to locate a suitable Python interpreter.
*   It handles the creation of a virtual environment and installation of necessary dependencies automatically.

## Extension Settings

This extension contributes the following settings:

*   `kapitan.inventoryPath`: Path to the inventory directory, relative to the workspace root. (Default: `inventory`)
*   `kapitan.YAMLExtension`: The extension used for classes and targets in the inventory. Options: `yml`, `yaml`. (Default: `yml`)
*   `kapitan.showDebugLogs`: Enable to show debug logs in the output channel. (Default: `false`)

## Developing the Extension

For instructions on how to build, run, and modify this extension, please verify the [Development README](https://github.com/kapicorp/kapitan-vscode-extension/blob/main/README_DEV.md).

## Copyright and License

This project is licensed under the Apache 2.0 License.

**Note**: The typescript code is a modified copy of the `client` folder from [Torque VS Code Extensions](https://github.com/QualiTorque/torque-vs-code-extensions), which was licensed under Apache 2.0 License. The initial folder structure, VSCode setup, and CI pipelines were also influenced by that repository.