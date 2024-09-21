pacmd set-default-sink alsa_output.usb-C-Media_Electronics_Inc._USB_Audio_Device-00.analog-stereo
pacmd set-default-source alsa_input.usb-046d_Logitech_StreamCam_2E50BCA5-02.iec958-stereo
xrandr --fb 1920x1080
xrandr --fb 1024x600
echo pill | sudo chmod 666 /dev/ttyCH341USB0
python /home/pill/smart-pill-box/app/main.py