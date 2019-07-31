# Command and Conquer 3 Mod Installer/Launcher

<p align="center">
 <strong>>>>>>>>>>>RELEASE v1.1 NOW AVAILABLE<<<<<<<<<<</strong>
</p>

 A simplistic mod installer/launcher for use with Command and Conquer 3 in the Command and Conquer Ultimate Edition.
 
 This mod installer is mainly intended for those with the Origin version of the Command and Conquer Ultimate Edition game as its CNC3 executables have command line options disabled, making the option for running a direct mod launcher nearly impossible. This launcher may also work with non-Origin versions of the Ultimate Collection (don't know, don't own those versions; will try to enable functionality though).
 
 Written in Python and compiled into an executable with PyInstaller, this launcher simply copies the files of whichever mod you choose and places the copied data into its respectful directories within the core game folder(s), allowing the mod to be played.
 
 **Note:** This launcher only works with mods that solely use .big and .skudef files. If your mod only has .ini files or whatever, this launcher does not support that type of installation (but I will happily add such functionality if need be).
 
 I may or may not include other games from the Ultimate Edition (Generals, Zero Hour, Red Alert 3, etc.) since I personally don't use them, and I currently have no knowledge of how to manually install mods to them.
 
 ***DISCLAIMER:*** Any copyrighted work within this repository (images, etc.) belong to their original creators/owners, not me. If any issues arise concerning copyrighted material, please post an issue; I will see it and tend to it accordingly.
 
 <br></br>

<p align="center">
  <img src="https://github.com/Medstar117/cnc3-mod-installer/blob/master/launcher.PNG">
</p>
 
 <br></br>
 
 # How To Use
  
 1. ***Add your mod (above mods listed are not included)*** - The launcher automatically generates a folder labeled "CNC3 Mods" located at "C:/Users/CURRENT USER/Documents/"; within that folder is a "Tiberium Wars" and a "Kanes Wrath" folder. Simply place your desired mod's folder into its respectful game folder. Then let the launcher do the rest--it will find all .skudef and .big files for your mod, even if there are other files within your mod's folder.
 
 2. ***Start the executable*** - Initially, the executable will take a bit of time to load as it has to find where "CNCLauncher.exe" is located on your system; after the first run, it will load very quickly as it will have that information saved to a path.info file.
 
 3. ***Select your game and mod*** - In the picture above, you will see 2 sections: the game list and the mod list. Select which game you want to play on the left, and the mods related to it will be listed on the right. Just select which mod you want to play and click the "Play Mod" button--the launcher will then install the mod and run "CNCLauncher.exe"; alternatively, you can select the "Play Vanilla" button, which will ensure that your game's directory is cleaned of mods before running "CNCLauncher.exe".
 
 4. ***Enjoy!*** - Your mod has been installed! After pressing either "Play Mod" or "Play Vanilla", the retail "CNCLauncher.exe" will run and you will have to select which game you want to play like normal. That's it!
 
 # >>>CNC Online Users<<<
  If you currently use CNC-Online's multiplayer launcher and want to use your mods online, then you're in luck! Make sure that you hook your games within CNC-Online's launcher so that your games have the ability to play online. Afterwards, run the mod launcher in accordance with the steps above; the retail "CNCLauncher.exe" will run like normal, but it does not matter which of the two games you select. After selecting either game, the CNC-Online launcher will open--from there you must select which game you want to play.
