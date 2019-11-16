# Get apk
* start android studio
* configure->AVD Manager (pin 0000)
* start an android emulator with Google Play.

```
C:\Users\markus\sdk-tools-windows-4333796\platform-tools>adb devices
List of devices attached
emulator-5554   device
```
You might need to wipe the emulator data if unathorized
download avanza from store / update avanza

List packages
```
adb shell pm list packages
...
package:se.avanzabank.androidapplikation
...
```

get path to apk
```
adb shell pm path se.avanzabank.androidapplikation

C:\Users\markus\sdk-tools-windows-4333796\platform-tools>adb shell pm path se.avanzabank.androidapplikation
package:/data/app/se.avanzabank.androidapplikation-ThISA0goX2UfuD2L0aTJmA==/base.apk
package:/data/app/se.avanzabank.androidapplikation-ThISA0goX2UfuD2L0aTJmA==/split_config.en.apk
package:/data/app/se.avanzabank.androidapplikation-ThISA0goX2UfuD2L0aTJmA==/split_config.xxhdpi.apk
```

transfer apk
```
pull apk
adb pull /data/app/se.avanzabank.androidapplikation-ThISA0goX2UfuD2L0aTJmA==/base.apk
adb pull /data/app/se.avanzabank.androidapplikation-ThISA0goX2UfuD2L0aTJmA==/split_config.en.apk
adb pull /data/app/se.avanzabank.androidapplikation-ThISA0goX2UfuD2L0aTJmA==/split_config.xxhdpi.apk
```

# Disassemble

* move apk:s to a nice new folder
* use https://github.com/skylot/jadx
* for each apk
  * create a folder with apk name, (eg. base)
  * open apk file, (eg. base)
  * file->save as gradle project


# Patch for MITM

* Download apktool from https://ibotpeaches.github.io/Apktool/
* Unpack apk file: apktool d base.apk
* Modify AndroidManifest.xml by adding `android:networkSecurityConfig="@xml/network_security_config"` attribute to application element.
* Remove requiredSplit attribute from application element
* Create file /res/xml/network_security_config.xml with following content:
```
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config>
        <trust-anchors>
            <certificates src="system" />
            <certificates src="user" />
        </trust-anchors>
    </base-config>
</network-security-config>
```
* Build patched apk: apktool b -o base_patched.apk --use-aapt2 base
* Use Java SDK to generate keys to sign apk:
```
"C:\Program Files\Java\jdk1.8.0_181\bin\keytool" -genkey -alias keys -keystore keys
```

* Sign apk file: jarsigner -verbose -keystore keys base_patched.apk keys
