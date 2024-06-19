
If dll or any of the files cannot be downloaded: <br>

First you must use MSYS2 to compile the C code <br>
You can download it here: https://www.msys2.org/ <br>
<br>
You must install MinGW64 on UCRT64 by following the command:<br>
pacman -S mingw-w64-ucrt-x86_64-gcc<br>
(it should take up to 30 minutes of downloading and installing)<br>
<br>
then check the following command<br>
gcc --version<br><br><br>
After that to compile the .dll and .lib and .so file you need to type this in the MSYS2 UCRT:<br>
REMEBER TO DIRECT THE UCRT FIRST: <br>
For example: cd /e/Data\ Data/Kuliah/Semester\ 2/Kerjaan\ Matkul/Data\ Structure/Lab/Final\ project <br>
then check the file using: ls <br><br>
If the directory is correct do the following command to install the dll, lib, and so files:<br>
.dll: gcc -shared -o gabung.dll gabung.c -O2 -Wall <br> 
.lib: gcc -shared -o gabung.dll -Wl,--out-implib,gabung.lib gabung.c <br>
.so: gcc -shared -o libgabung.so gabung.c <br>


-----------------------------------------------------------------------

<br>
Python version: 3.12.4 ==> install it here: https://www.python.org/downloads/release/python-3124/<br>
<br>
Libraries that we used for GUI:<br><br>

1. numpy ==> installation guide: https://numpy.org/install/ ==> in terminal: pip install numpy<br><br>

2. matplotlib ==> installation guide: https://matplotlib.org/stable/install/index.html ==> pip install matplotlib<br><br>

3. tkinter ==> installation guide: https://www.tutorialspoint.com/how-to-install-tkinter-in-python ==> pip install tk<br><br>

4. Pillow ==> installation guide: https://pypi.org/project/pillow/ ==> pip install pillow<br><br>
<br>




