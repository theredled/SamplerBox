FORK NOTES: 

* Makes Samplebox compatible with Python 3.9+, including using `python-rtmidi` module instead of `rtmidi-python`.
* Refactored source code for OOP and remote usage
* No support for loops for the moment.
* GPIO buttons, Serial MIDI and 7-degment display are not tested.

Modified README:

# SamplerBox

SamplerBox is an **open-source DIY audio sampler project** based on RaspberryPi.

Website: [www.samplerbox.org](https://www.samplerbox.org)

[![](https://gget.it/flurexml/1.jpg)](https://www.youtube.com/watch?v=yz7GZ8YOjTw)

# Install

SamplerBox works with the RaspberryPi's built-in soundcard, but it is recommended to use a USB DAC (PCM2704 USB DAC for less than 10€ on eBay is fine) for better sound quality. 

0. Start with a standard Rasperry PI OS install. The following steps have been tested with Legacy Rasperry Pi OS/Raspbian 11 (Bull's Eye) on RPi 3B

1. Install the required dependencies (Python-related packages and audio libraries - the current version requires at least Python 3.7):

    ~~~
    sudo apt update
    sudo apt -y install git python3-pip python3-smbus python3-numpy libportaudio2 
    sudo apt -y install raspberrypi-kernel  # quite long to install, do it only if necessary, it solves a "no sound before 25 second on boot" problem
    sudo pip3 install cython python-rtmidi cffi sounddevice pyserial
    ~~~
    
2. Download SamplerBox and build it with:

    ~~~
    git clone https://github.com/theredled/SamplerBox.git
    cd SamplerBox
    sudo python3 setup.py build_ext --inplace
    ~~~

3. Reboot the Pi, and run the soft with: 
    
    ~~~
    sudo python3 samplerbox.py
    ~~~

    Play some notes on the connected MIDI keyboard, you'll hear some sound!

4. Copy `samplerbox_src/config.py.sample` to `samplerbox_src/config.py`

5. *(Optional)*  Modify `samplerbox_src/config.py` if you want to change root directory for sample-sets, default soundcard, etc.


# How to use it

See the [FAQ](https://www.samplerbox.org/faq) on https://www.samplerbox.org.
Fork note: Default root directory for sample-sets is now `samples/`

# About

Fork Author : Benoît Guchet (twitter: [@Yoggghourt](https:/twitter.com/yoggghourt), mail: [benoit.guchet@gmail.com](mailto:benoit.guchet@gmail.com))
Original Author : Joseph Ernest (twitter: [@JosephErnest](https:/twitter.com/JosephErnest), mail: [contact@samplerbox.org](mailto:contact@samplerbox.org))

# License

[Creative Commons BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)
