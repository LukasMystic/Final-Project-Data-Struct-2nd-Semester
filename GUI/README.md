
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
then check the file using: ls <br>
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

-----------------------------------------------------------------------
<br>
You can find all the link for the backup files here: <br>
<br><br>

Link Onedrive: https://binusianorg-my.sharepoint.com/personal/mochammad_pasha_binus_ac_id/_layouts/15/guestaccess.aspx?share=EsEey2r6y1FFqBHjtDUu7e8BjzwdrAFOfsHlVq-S_f_4PQ&e=e3Mbrt
<br><br><br>

Link Canva(GitHub, Canva Public View, Semua Video, Jobdesk, dll): https://www.canva.com/design/DAGIYBJ09xI/e_HgiJpDiwP5B1zraa2a-g/view?utm_content=DAGIYBJ09xI&utm_campaign=designshare&utm_medium=link&utm_source=editor
<br><br><br>

Link Github: https://github.com/LukasMystic/Final-Project-Data-Struct-2nd-Semester/tree/main

<br><br><br>
Link Tutorial: https://binusianorg-my.sharepoint.com/personal/mochammad_pasha_binus_ac_id/_layouts/15/guestaccess.aspx?share=EWRtZ7dQEwNBjeyXyLCtE-EBv-5AHKpJ7PFhMGt1P-AVig&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=FqDhSp


