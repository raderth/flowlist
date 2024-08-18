
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
</ul>

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/P5P7YI0NT)

<hr>
<h1>Setup</h1>
<p>Make sure you get a server up and running. Get a more experienced person for this if you are likely to struggle, but you can setup any old machine you have(remember to port forward port 80)</p>
<p>I'm using linux here. Scroll down for windows</p>
<h2>requirements</h2>
<ul>
<li>A basic server with docker (there are a lot of free ones that will work fine for most people)</li>
<li>Ability to open port 80</li>
<li>Ability to open ports on minecraft server</li>
<li>Ability to download plugins on minecraft server</li>
</ul>
<h3>Step 1</h3>
<a href="https://discordpy.readthedocs.io/en/stable/discord.html">Make a discord bot</a><p>and write down the bot <b>token</b> the <b>client secret</b> and the <b>client ID</b>.</p>
<p>you also need to add a redirect for your server (not the minecraft one)</p>

![redirects](https://github.com/raderth/flowlist/blob/main/images/redirects.png?raw=true)

<h3>Step 2</h3>
Paste these commands into the linux console!
Install docker, sometimes it's preinstalled but running this wont do any harm

```
sudo apt-get install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
```
<h3>Step 3</h3>
Download the latest release of flowlist from releases. Then run it!

```
docker pull raderth/flowlist:beta
docker run -it raderth/flowlist:beta
```

<p>For it to be running even if the server crashes and reboots,</p>
<p>Try:</p>

```
vim /etc/systemd/system/flowlist.service
```

or,

```
nano /etc/systemd/system/flowlist.service
```

Add this to the file:

```
[Unit]
Description=flowlist
After=network.target

[Service]
Restart=always
ExecStart=/usr/bin/docker run --rm --name flowlist raderth/flowlist:beta
ExecStop=/usr/bin/docker stop flowlist

[Install]
WantedBy=multi-user.target
```

Enable at startup:

```
sudo systemctl enable flowlist.service
```

<h3>Step 4</h3>
Complete the configuration as prompted. In discord you need to use <b>/set</b> and <b>/add</b> to set the channel for applications and add to set who can use <b>/whitelist</b> and <b>/ban</b>

<h3>Step 5</h3>
Install the plugin and you should be good to go!

<h3>Step 6</h3>
I lied, to actually setup your form go to <your-ip/url>/admin and login. You set this password if you ran flowlist!

<hr>
Alternatively you can install docker desktop on an old windows machine. If you go into the settings you can make it boot on launch. I'll add more details on this at some point in the future

<h2>Discord Setup</h2>
<ul>
<li>use <b>/add</b> and <b>/remove</b> respectively to select who is allowed to use <b>/whitelist</b> and <b>/ban</b></li>
<li>use <b>/set</b> to select the channel that application will be sent in, make sure this is moderator only accessible</li>
<li>use <b>/role</b> to select the role that players recieve when accepted. You can use this to unlock certain channels in your discord</li>
</ul>

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/P5P7YI0NT)
