# Local Network Clipboard Sharing Tool

A Python-based tool that enables clipboard sharing between computers on a local network through a client-server architecture.

## User Stories

### As a user setting up the system
- I want to be able to easily start the clipboard server on my main computer
- I want to configure basic settings like port number and allowed IP addresses
- I want the server to run silently in the background without interfering with my work
- I want to see status messages confirming the server is running correctly

### As a client user
- I want to connect to the clipboard server by providing the server's IP address and port
- I want the client to run silently in the background
- I want to receive notifications when connection status changes
- I want to see error messages if connection fails

### As a user sharing clipboard content
- I want my clipboard content to automatically sync when I copy something
- I want to be able to paste content that was copied on another computer
- I want to share text, images and formatted content between computers
- I want clipboard history to be available across all connected devices
- I want to be able to disable sharing temporarily when copying sensitive information

### As a system administrator
- I want to restrict which computers can connect to the clipboard server
- I want to encrypt clipboard data being transmitted over the network
- I want to monitor connection attempts and clipboard activity
- I want to be able to revoke access for specific clients
- I want to set size limits for shared clipboard content

### As a security-conscious user
- I want all clipboard data to be encrypted in transit
- I want to be able to clear shared clipboard history
- I want to see which computers are currently connected
- I want to be notified when new devices connect to the server
- I want to manually approve new device connections
