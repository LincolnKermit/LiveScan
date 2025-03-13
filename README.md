
# LiveScan


⚠️ **This project is strictly for educational purposes only.** ⚠️

⚠️ **Since the Raspberry Pi lacks a GPS module, we'll use our phone to transmit the location.** ⚠️


## Documentation

![image](https://github.com/user-attachments/assets/f87f2881-390a-4199-bf66-4daa1f0f3ef4)




## Installation



### Launch the listener

**It should be launched before the server and on the same RPI.**

```bash
  git clone https://github.com/lincolnkermit/livescan
  cd livescan
  sudo bash Server/worker.sh
```



### Launch the Server




```bash
  git clone https://github.com/lincolnkermit/livescan
  cd livescan
  pip3 install flask
  python3 Server/app.py
```


The server is running on private_ip:1337


### Swift App

*For the GPS Coordinates : Convert the swift app into .ipa through XCode and run it into an iPhone as dev-mode.*


**Note : You can also send any POST Requests with longitude=x.xxxx, latitude=y.yyyyyyyy @ server:1337/upload_gps**


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

