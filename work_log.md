start 10.12.22
## 1 Pomo:
added logger
Added three buttons in Home Screen
Implemented Vanilla navigation with Screen Manager

## 2 Pomo:
додав addDataScreen і addDataCard
реалізував передачу input feature key-val from addDataScreenView -> addDataScreenController -> addDataScreenModel

reference for MVC patern in kivy
https://github.com/AlesyaRabushka/MVC_Kivy_Python

## 3 Pomo:
додав кнопку confirm в addDataScreen
додав запис в Json через модель

## 4 Pomo
Додав створення session_json при заході у SessionScreeView


## 10 Pomo
https://github.com/Kulothungan16/kivy-lazy-loading-template/blob/main/libs/uix/root.py
lazy loading with function for screens .goback()


## 11 Pomo:
Start debuging with my androind
1. Plug pphone with enabled debuuggin
2. On windows console check devices: adb devices 
set up adb tcpip 5555 
3. in linux 
    adb -s 7369ca370504 install myapp-0.1-arm64-v8a_armeabi-v7a-debug.apk
    adb -s 7369ca370504 logcat *:S python:D 


## 12 Pomo:
There are several potential risks and problems that can occur if you run the Buildozer tool as the root user:

Compatibility issues: Running Buildozer as root may cause compatibility issues with other software or tools, as the root user has full access to the system and may be able to make changes that could affect the behavior of other programs.
Maintenance issues: If you run Buildozer as root, you may encounter maintenance issues in the future, as it can be difficult to track and manage the changes that have been made to the system. This can make it more difficult to troubleshoot problems and perform system updates

Not critical as me

## 13 Pomo:
[WARNING] [Config      ] Older configuration version detected (0 instead of 24)
[Window      ] virtual keyboard not allowed, single mode, not docked
may be cues

## 14-16 Pomo:
added android permissions in 2 methods via 
1*.spec
2.in runtime 

*Indicated error with absolute path for json files to interact.* 
It was part of global error with crashing app on navigation to other screen from home 

Log error cue 1:
Logcat 
```12-19 23:22:14.246 30455 30475 I python  : [INFO   ] [KivyMD      ] 1.1.1, git-Unknown, 2022-12-19 (installed at "/data/user/0/org.aappdomain.aapp/files/app/_python_bundle/site-packages/kivymd/__init__.pyc")
12-19 23:22:14.254 30455 30475 I python  : [INFO   ] [Factory     ] 189 symbols loaded
12-19 23:22:20.727 30493 30493 F DEBUG   : Build fingerprint: 'xiaomi/tissot/tissot_sprout:9/PKQ1.180917.001/V10.0.24.0.PDHMIXM:user/release-keys'
12-19 23:22:20.727 30493 30493 F DEBUG   : Revision: '0'
12-19 23:22:20.727 30493 30493 F DEBUG   : ABI: 'arm64'
12-19 23:22:20.727 30493 30493 F DEBUG   : pid: 30455, tid: 30475, name: SDLThread  >>> org.aappdomain.aapp <<<
12-19 23:22:20.727 30493 30493 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x38
12-19 23:22:20.727 30493 30493 F DEBUG   : Cause: null pointer dereference
12-19 23:22:20.727 30493 30493 F DEBUG   :     x0  000000794bdca800  x1  0000000000000003  x2  0000000000000000  x3  0000000000000000
12-19 23:22:20.727 30493 30493 F DEBUG   :     x4  0000000000008cd5  x5  000000794bcad180  x6  0000000000008cd5  x7  000000794e47c6c0
12-19 23:22:20.727 30493 30493 F DEBUG   :     x8  0000000000000040  x9  0000000000000001  x10 0000000000000001  x11 0000000000000000
12-19 23:22:20.727 30493 30493 F DEBUG   :     x12 0000000000000001  x13 000000794bcad210  x14 00000000000000ff  x15 0000000000000000
12-19 23:22:20.727 30493 30493 F DEBUG   :     x16 0000000000000000  x17 0000000000000001  x18 0000000000000002  x19 000000794e47c6c0
12-19 23:22:20.727 30493 30493 F DEBUG   :     x20 0000000000000000  x21 0000000000008be7  x22 0000000000000001  x23 0000000000000000
12-19 23:22:20.727 30493 30493 F DEBUG   :     x24 000000794bcad210  x25 000000000000003c  x26 000000794e47ca50  x27 0000000000000058
12-19 23:22:20.727 30493 30493 F DEBUG   :     x28 0000000000000000  x29 000000794f3fc0a0
12-19 23:22:20.727 30493 30493 F DEBUG   :     sp  000000794f3fc040  lr  000000795f223630  pc  000000795f223bd8

12-19 23:22:20.540 30455 30475 F libc    : Fatal signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x38 in tid 30475 (SDLThread), pid 30455 (aappdomain.aapp)
```

## 17 Pomo:
Decided to store sessions json at path
/data/data/org.test.aapp/files/app/assets/data
in adroid app internal storage.

DIRECTORY                                                    DESCRIPTION / API
=====================================================================================
APP CODE
========
/data/app/<pkg>*                                             (user apps installation directory)
/data/app/<pkg>*/base.apk                                    (original `.apk` file)
/data/app/<pkg>*/lib/<arch>/*.so                             (shared libraries)
/data/app/<pkg>*/oat/<arch>/base.[art|odex|vdex]             (compiled executable code)
/data/dalvik-cache/<arch>/*.[art|dex|oat|vdex]               (compiled executable code, only for system apps)
/data/misc/profiles/cur/<user_id>/<pkg>/primary.prof         (ART profile)
/data/misc/profiles/ref/<pkg>/primary.prof                   (ART profile)

INTERNAL STORAGE
================
/data/user[_de]/<user_id>/<pkg>                              getDataDir
/data/user[_de]/<user_id>/<pkg>/files                        getFilesDir
/data/user[_de]/<user_id>/<pkg>/[code_]cache                 getCacheDir or getCodeCacheDir
/data/user[_de]/<user_id>/<pkg>/databases                    getDatabasePath
/data/user[_de]/<user_id>/<pkg>/no_backup                    getNoBackupFilesDir
/data/user[_de]/<user_id>/<pkg>/shared_prefs                 getSharedPreferences

EXTERNAL STORAGE
================
/storage/emulated/obb/<pkg>/*.obb                            (shared by multi-users, exposed in following view)
/storage/emulated/<user_id>/Android/obb/<pkg>/*.<pkg>.obb    getObbDirs
/storage/emulated/<user_id>/Android/media/<pkg>              getExternalMediaDirs
/storage/emulated/<user_id>/Android/data/<pkg>/             
/storage/emulated/<user_id>/Android/data/<pkg>/files         getExternalFilesDirs
/storage/emulated/<user_id>/Android/data/<pkg>/[code_]cache  getExternalCacheDirs

 
## 18 Pomo:
add handling on_pause, on_resume, on_start at MDApp lvl to prevent reboot
more Loggers

## 19 Pomo:
had tried different strategies to resolve Issue with app crash
1. Target api build.
2. Tests on Android Device Manager emulator, face issue with termination of device session, skipped.
3. Unlock runtime andoid permission for external storage, but decided that it not cause of problem
4. Analyzed logcat, but it led to misconception about cause. Memory leak and tombstones made me think that I have not supported Android on debug phone.

## 20 Pomo:
```requirements = python3,pillow,android,sdl2_ttf==2.0.15,kivy==2.1.0,kivymd==1.0.2``` in .spec
especially kivymd==1.0.2
resolves critical signal 11 and SDLThread ISSUE#1 
that occurs when I was trying to navigate forward to other screens, after android build 


## 20-25 Pomo:
add vanilla uploading to Google Sheets
bruteforce requirements for gspread lib in buildozer.spec:

```
requirements = python3,pillow,android,kivy==2.1.0,kivymd==1.0.2,google-auth-oauthlib,oauthlib,requests_oauthlib,httplib2,pyasn1,pyasn1-modules,requests,rsa,oauth2client,urllib3,chardet,gspread,google-auth,cachetools,idna
```

Done some refactoring
Add empty txt filler to avoid OS not existing data folder (vanilla bone)


## 25-30 Pomo:
use
```py .\main.py -m screen:nexus7.2,portrait,scale=0.75```
for testing on different screens
```py main.py -m screen``` list all available screens

Problem with displaying layouts on android screen occurred, 
but with simulated screen it doing well:
update kv files to use dp metrics for displaying widgets, and sp for text

Resolved problem with fitting MDSegmentControl
Fixed distance btw AppBar and Other view, also 

## 30-35 Pomo:
Done with suggestions for Tree Specie TextField, it consists of:
 - initialization in Session Screen controller pandas element, build for .spec included setting ```pandas=1.0.3```
In forums was point to switch ```p4a.branch = develop``` but it worked without it
 - Selecting among available Goggle worksheets in one document on uploading, initialized in Session Screen Model
 - Issue with RecycleView was persisted


## 35-40 Pomo:
 - Placed worksheet choosing as new button at Home Screen
 - Added and modified items preview in Session Screen and Add Data Screen 
 - Finish Uploading to Google sheet in right format
 - Seems like resolve Issue with RecycleView, need build to check
 - Added New Screen - PhotoScreen, make vanilla version according to provided example for using module Camera4Kivy


## 40-45 Pomo:
 - Tested on other Android device. Camera works for Android 10 devices but crash on Android 9

## References:
1. [updating recycle view](https://medium.com/nerd-for-tech/how-to-refresh-kivy-recycleview-72244883d075)

2. [app Optimization Methods](https://gist.github.com/Guhan-SenSam/9dfb11b7bfd8fd24561f4fcd9ff0d5de)

3. [example of using camera4kivy](https://github.com/Android-for-Python/c4k_photo_example)

