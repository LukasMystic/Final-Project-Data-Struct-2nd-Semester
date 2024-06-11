You must use MSYS2 <br>
You can download it here: https://www.msys2.org/ <br>
You must install MinGW64 on UCRT64 by following the command:<br>
pacman -S mingw-w64-ucrt-x86_64-gcc<br>
(it should take up to 30 minutes of downloading and installing)<br>
<br>
then check the following command<br>
gcc --version<br><br>
After that if you want to compile the .dll and .lib and .so file you need to type this in the MSYS2 UCRT:<br>
REMEBER TO DIRECT THE UCRT FIRST: <br>
For example: cd /e/Data\ Data/Kuliah/Semester\ 2/Kerjaan\ Matkul/Data\ Structure/Lab/Final\ project <br>
then check the file using: ls <br>
.dll:gcc -shared -o gabung.dll gabung.c -O2 -Wall <br> 
.lib:gcc -shared -o gabung.dll -Wl,--out-implib,gabung.lib gabung.c <br>
.so: gcc -shared -o libgabung.so -fPIC gabung.c <br>
