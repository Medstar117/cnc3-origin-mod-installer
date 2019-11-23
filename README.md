# Command and Conquer 3 Mod Installer/Launcher

<p align="center">
 <a href="https://github.com/Medstar117/cnc3-origin-mod-installer/releases/download/v1.3/CNC3_Mod_Installer.exe">
  <span>
   <strong>>>>>>>>>>>DOWNLOAD RELEASE v1.3<<<<<<<<<<</strong>
  </span>
 </a>
</p>

 ***NOTICE: YOU MUST HAVE PATCH 1.09 FOR TIBERIUM WARS, PATCH 1.02 FOR KANE'S WRATH, PATCH 1.12 FOR RED ALERT 3, AND PATCH 1.0 FOR UPRISING!!!***

 ***NOTICE 2:*** As of right now, whenever you press the "Play Mod" button, the mod will stay installed until you press the "Play Vanilla" button. Later on down the road, I may add a process monitoring hook into place so that the game is restored whenever the user exits the program. So, if you use this, then you had better get used to it!

 # Description

 ***-----------------------------------------------READ ABOVE BEFORE PROCEEDING-----------------------------------------------***

 A simplistic mod installer/launcher made for use with Command and Conquer 3 in the Command and Conquer Ultimate Collection.

 This mod installer is mainly intended for those who own Command and Conquer: The Ultimate Collection on Origin as its CNC executables have command line options disabled, making the option for running a direct mod launcher nearly impossible. This launcher also works with non-Origin versions of Command and Conquer 3 (funtionality enabled in v1.2).

 Written in Python and compiled into an executable with PyInstaller, this launcher simply copies the file paths of a mod's .skudef file and edits the core CNC3 .SkuDef file, forcing the game to read the custom data files, allowing the selected mod to be played.

 **Note:** This launcher only works with mods that solely use .big and .skudef files. If your mod only has .ini files or whatever, this launcher does not support that type of installation (but I will happily add such functionality in the future).

 I will include other games from the Ultimate Edition (Generals, Zero Hour, Red Alert 3, etc.) that are modifyable whenever I gain the knowledge on how to modify each game.

 ***DISCLAIMER:*** Any copyrighted work within this repository (images, etc.) belong to their original creators/owners, not me. If any issues arise concerning copyrighted material, please post an issue; I will see it and tend to it accordingly.

 <br></br>

<p align="center">
  <img src="https://github.com/Medstar117/cnc3-mod-installer/blob/master/launcher.PNG">
</p>

 <br></br>

 # How To Use

 1. ***Add your mod (above mods listed are not included)*** - The launcher automatically generates a folder labeled "CNC Mods" located at "C:/Users/CURRENT USER/Documents/"; within that folder are folders corresponding to each supported game. Simply place your desired mod's folder into its respectful game folder, then let the launcher do the rest--it will find all .skudef and .big files for your mod, even if there are other files within your mod's folder.

 2. ***Start the executable*** - Initially, the executable will take a bit of time (about 30 seconds) to load as it has to locate all of the CNC3 executables on your system; after the first run, it will load very quickly as it will have that information saved to a "path_locations.info" file.

 3. ***Select your game and mod*** - In the picture above, you will see 2 sections: the game list and the mod list. Select which game you want to play on the left, and the mods related to it will be listed on the right. Just select which mod you want to play and click the "Play Mod" button--the launcher will then install the mod and run the appropriate executable; alternatively, you can select the "Play Vanilla" button, which will ensure that your game's directory is cleaned of mods before running the appropriate executable.

 4. ***Enjoy!*** - Your mod has been installed! After pressing either "Play Mod" or "Play Vanilla", the desired game will run. For TUC users, the standard "CNCLauncher" window will open--just select what game you want on there like normal; there is no bypass to that extra window opening. That's it!

 # >>>CNC Online Users<<<
  If you currently use CNC-Online's multiplayer launcher and want to use your mods online, then you're in luck! Make sure that you hook your games within CNC-Online's launcher so that your games have the ability to play online. Afterwards, run the mod launcher in accordance with the steps above. The CNC-Online launcher will open like normal, and you will have to select again which game you want to play.
