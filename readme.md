



![header](https://github.com/raderth/flowlist/blob/main/images/header.png?raw=true)

<h1>Description</h1>
<p>Flowlist makes whitelisting easy for moderators and owners by integrating an application form with discord and then minecraft</p>
<p>Most interactions will take place with a discord bot.</p>
<p>You can edit the application form through an admin panel...</p>

![confirm](https://github.com/raderth/flowlist/blob/main/images/confirmation.png?raw=true)

<p>The bot will inform users once they successfully submit an application...</p>

![form](https://github.com/raderth/flowlist/blob/main/images/form.png?raw=true)

<p>and the details will be sent to a channel of your choosing</p>

![application](https://github.com/raderth/flowlist/blob/main/images/application.png?raw=true)

<p>Accepting will then add the user to the whitelist in addition to any role you want added</p>
<p>For conveinience this bot also includes the following commands:</p>
<ul>
<li>/whitelist</li>
<li>/ban</li>
<li>/cmd</li>
</ul>

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/P5P7YI0NT)

<hr>
<h1>Setup</h1>
<p>Make sure you get a server up and running. Get a more experienced person for this if you are likely to struggle, but you can setup any old machine you have(remember to port forward port 80 on this server, this might already be done depending on your setup)</p>

## Requirements
- Any basic Linux server with Docker installed
- Ability to open port 80 and Minecraft server ports (e.g., 25575 for RCON, 8080 for plugin API)
- Ability to install plugins on your Minecraft server

---

## Discord Bot Setup
1. [Create a Discord bot](https://discordpy.readthedocs.io/en/stable/discord.html)
2. Note the **token**, **client ID**, and **client secret**
3. Add a **redirect URI** pointing to your web server

![redirects](https://github.com/raderth/flowlist/blob/main/images/redirects.png?raw=true)

---


## Minecraft Server Setup
1. Open `server.properties`
2. Set: 
```
enable-rcon=true
rcon.password=your_secure_password
```
3. Open the **RCON port** (default: `25575`)
4. You'll enter this port and password during Flowlist setup

---


## Install
#### **Most servers (linux)**
Run this:
```
curl -fsSL https://github.com/raderth/flowlist/releases/latest/download/install.sh -o install.sh && bash install.sh
```


#### **Windows**
1. Get the exe in releases.
2. Create a shortcut to your `.exe` in:
```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
```

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/P5P7YI0NT)

