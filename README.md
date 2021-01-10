# apkbleach.com

Visit: https://apkbleach.com

A central version of ApkBleach on a web page to eliminate install issues of apkbleach.py accross differing systems.

# About
ApkBleach was developed specifically to obfuscate android payloads generated by the metasploit-framework in attempts to evade detection. The obfuscation that takes place attempts to evade detection with two main methods. The first method is strictly for screening of the decompiled payload. By default metasploit generates a android application littered with the keywords metasploit and payload. Replacing those keywords with random strings and randomizing file names is good first step in obfuscating the typical metasploit android payload. The next method is to change the way the payload is executed. The default payload generated by metasploit executes on create or simply put as soon as the application is opened. This obfuscation method uses the devices accelerometer activity to launch the payload. So the apkbleach payload will wait for physical movement of the target device before executing the payload. In addition to those obfuscation techniques apkbleach automates the process of changing the metasploit app icon and name.

# Features
* Custom App name
* Choice in payload and options
* Obfuscation
* Changing the PAYLOAD to be executed on the devices accelerometer activity
    * Using the accelermoter to trigger the payload also gives us the ability to choose how many sessions we want to spawn on launch.
* Icon iojection
* App permissions editing

![Screen shot of sofware image](https://github.com/graylagx2/Images/blob/master/apkbleach_home.png)
![Screen shot of sofware image](https://github.com/graylagx2/Images/blob/master/apkbleach_download.png)
