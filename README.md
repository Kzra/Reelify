# Reelify
**Summary**: This program is designed to give you the last t seconds of a recording when you press a hotkey. 
It is useful to capture moments of creativity without having to curate an entire recording, for example during a jam or brainstorming session.
The program uses Pyaudio to continually stream audio data into a numpy array of fixed size [t * samplerate] which overwrites as it is filled. 
The array is saved as a .wav file when the hotkey is pressed. 

**Dependencies**: The program is written in Python 3 and requires the following non-standard modules to run: 
[PyAudio](http://people.csail.mit.edu/hubert/pyaudio/), [SciPy](https://www.scipy.org/), [NumPy](http://numpy.org/) and [Keyboard](https://github.com/boppreh/keyboard). 

**Usage**:
```shell 
python reelify.py [-t] [-k] [-d] [-f] [-b] [-s]
```

```[-t]```: set the length of the recording to save (optional, you will be prompted if not given). 

```[-k]```: the key to press to save the current recording (optional, default: 'space'). 

```[-d]```: folder to save the recordings into (optional, default: '.'). 

```[-f]```: generic name to give the recording files (optional, default: 'test'). 

```[-b]```: buffer size (optional, default: 1024). 

```[-s]```: sample rate (optional, default: 44100). 

**Example**:

 ![Example](https://github.com/Kzra/Reelify/blob/master/Reelify_command_prompt.png)

**Acknowledgements**: Thanks to my friend Henry for his advice on the program design. 

**Future Developments**:
- Voice activation of the hotkey, for example when the user says 'Reelify'.
- Develop a G.U.I.
- Port the program to IOS/Android. 

