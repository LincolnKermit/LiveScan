
# LiveScan


⚠️ **This project is strictly for educational purposes only.** ⚠️

⚠️ **Since the Raspberry Pi lacks a GPS module, we'll use our phone to transmit the location.** ⚠️


## Documentation

![image](https://github.com/user-attachments/assets/57354cfe-70cf-441a-8af9-155ef635ea93)



## Installation

### Launch the Server

```bash
  git clone https://github.com/lincolnkermit/livescan
  cd livescan
  pip3 install flask
  python3 Server/app.py
```
The server is running on private_ip:1337

### Launch the App

*Convert the swift app into .ipa through XCode and run it into an iPhone as dev-mode.*
## Tech Stack

**Client:** Swift

**Server:** Flask RESTful API



**SwiftUI**: For building the user interface.

**CoreLocation** ( Swift Lib ) : For accessing and tracking GPS coordinates.

**Flask**: A lightweight Python web framework for handling and 
processing incoming data on the server.

**airmon-ng**: A command-line tool for enabling monitor mode on 
wireless interfaces to scan nearby networks.

**RESTful API Communication**: For sending GPS data to the remote 
server using HTTP POST requests.



## Authors

- [@LincolnKermit](https://www.github.com/LincolnKermit)

