#usr/bin.env/python3
"""
    ***********************Reelify.py*****************************************************************************
    This program is designed to give you the last t seconds of a recording when you press a hotkey. 
    It is useful to capture moments of creativity without having to curate an entire recording.
    The program uses Pyaudio to continually stream audio data into a numpy array of fixed size, which overwrites once filled. 
    The array is saved as a .wav file when the hotkey is pressed. 
"""

#Modules
import pyaudio
import numpy as np
import keyboard
import scipy.io.wavfile
import argparse
import os


#Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-t","--record_time",type=int, help="length of recording to save (you will be prompted in the script if not given)")
parser.add_argument("-k","--hot_key",type=str,help="the key to press to save the current recording (default = 'space')")
parser.add_argument("-d","--directory",type=str,help="folder to save the recordings into (default = '.')")
parser.add_argument("-f","--file_name",type=str,help="generic name to give the recording files (default = 'test')")
parser.add_argument("-b","--buffer_size",type=int,help="buffer size (default = '1024')")
parser.add_argument("-s","--sample_rate",type=int,help="sample rate (default = '44100')")
args = parser.parse_args()

if args.record_time: 
    listen_time = args.record_time
else:
    listen_time = int(input('How many seconds previous would you like to save? '))


if args.hot_key:
    hotkey = args.hot_key
else:
    hotkey = 'space'

if args.directory:
    os.mkdir(args.directory)
    os.chdir(args.directory)

if args.file_name:
    filename = args.file_name
else:
    filename = 'test'

if args.buffer_size:
    BUFFERSIZE = args.buffer_size
else:
    BUFFERSIZE = 1024 # fixed buffer size
 
if args.sample_rate:
    Sample_rate = args.sample_rate
else:
    Sample_rate = 44100

    
#Other Variables
Buff_per_sec = round(Sample_rate/BUFFERSIZE)
numpydata = np.zeros(shape=(BUFFERSIZE * Buff_per_sec * listen_time),dtype=np.int16) #recording file
rn = 1


"""
Buffer Size / Sample Rate / Bit Depth

Reference: https://support.focusrite.com/hc/en-gb/articles/115004120965-Sample-Rate-Bit-Depth-Buffer-Size-Explained

The Sample rate will be the number of audio samples that are captured per second and is measured in Hertz.

Common Sample Rates: 44.1, 48, 88.2, 96, 176.4, 192 (kHz)

This means that as you increase the sample rate, more data is captured per second.

 

Bit depth is the number of “bits” captured in each sample per second.

As this changes so does the dynamic range which is the difference between the lowest and highest volume of a signal that can be recorded. As you increase bit depth, you expand the threshold of what can be heard and recorded by your recording software although the maximum range of human hearing typically does not exceed 120 dB.

Common Bit Depths: 16, 24

 

Buffer Size is the amount of time allowed for your computer to process the audio of your sound card, or audio interface.

This applies when experiencing latency, which is a delay of processing audio in real time. You can reduce your buffer size to limit latency but this can result in a higher burden on your computer which can cause glitchy audio or drop-outs.

This can generally be fixed by increasing your buffer size in the audio preferences of your DAW or driver control panel.
                                                                      
                                                                      """


print('\nPress esc to exit. \n\nPress ',hotkey,' to save the last ',listen_time,' seconds.\n')
# initialize portaudio
p = pyaudio.PyAudio()

#begin the recording session
print("*"*50)
#stream data into the numpy array. every listen_time seconds rewrite the array from element 0.
stream = p.open(format=pyaudio.paInt16, channels=1, rate=Sample_rate, input=True, frames_per_buffer=BUFFERSIZE)
proc = True
while proc is True:
            reelify = True
            print('\nListening...')
            while reelify == True:       
                for i in range(0,(Buff_per_sec * listen_time)):
                        data = stream.read(BUFFERSIZE)
                        numpydata[i*BUFFERSIZE:((i+1)*BUFFERSIZE)] = np.frombuffer(data, dtype=np.int16)
                        if keyboard.is_pressed(hotkey):
                            reelify = False
                            break
                        if keyboard.is_pressed('esc'):
                            reelify = False
                            proc = False
                            break
            
            #don't do any processing if esc has been pressed
            if proc == False:
                break
            
            #forget the hotkey press 
            while keyboard.is_pressed(hotkey):
                pass
                        
            #plot un_ordered data
            #plt.plot(numpydata)
            #plt.show()
            
            #reorder the data
            roll_param = len(numpydata)-(i+1)*BUFFERSIZE
            numpydata = np.roll(numpydata,roll_param)
        
            # plot ordered data
            #plt.plot(ord_numpy_data)
            #plt.show()
        
            #write the audio
            scipy.io.wavfile.write((filename+str(rn)+'.wav'), Sample_rate, numpydata)
            print('Recording saved as ',filename,str(rn),'.wav')
            rn += 1 
  
# close stream
stream.stop_stream() 
stream.close()  
print('\nExiting!')
