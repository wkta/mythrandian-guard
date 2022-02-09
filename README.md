# Mythrandian Guard

<center>
<a href="https://discord.gg/24DfrtvpXk"><img src="discord-logo.png" height="48"></a>
</center>

A game of Heroes and Lackeys\
*Un jeu de Héros et de Laquais*

## Type of game / Type de jeu

Idle-game + "Deck building" game


## Gameplay overview / Aperçu du gameplay

You start with a hero, you collect new gear and new Lackeys by picking up missions. A selected mission needs to be hard enough so your rewards are worthy, but not too hard otherwise your hero/team is wounded and you loose some time generally speaking (->no progress made).

*Tu démarres avec un héros, tu collectionnes du nouveau matériel et de nouveaux Laquais via la sélection de missions. Une mission sélectionnée doit être suffisament difficile de manière à produire des récompenses de valeur, mais pas trop difficile autrement ton héros/équipe est blessée et tu perds du temps de manière générale (->absence de progression).*

## Chosen tech stack (overview)

Python and the katagames SDK on the client-side,\
PHP on the server-side.

*Python et le SDK katagames côté client,*\
*PHP sur le côté serveur.*


## Development: client-side

Main file for now is `main.py`
in order to run this game, you need the katagames_sdk (nightly build)
that can be found via `github.com/gaudiatech`. Check the repo named `katasdk-public`.
There, you can grab `src\katagames_sdk` and simply copy the folder inside the `client\` folder
of the current project. Congrats, you can run the game client now!

## Development: server-side

(Proof-tested using Ubuntu 21.10, should work with any Linux system)

First install software for running http servers:
apache and mysql...You can follow this tutorial:
`https://www.linuxhelp.com/how-to-install-lamp-setup-on-ubuntu-21`


```
$ sudo apt install apache2
$ sudo apt install mysql-server  # or mariadb-server mariadb-client
```
remember you may need to open access on `public_html` so apache
can read users files, example:
```
a2enmod userdir
chmod 755 /home/tom
mkdir /home/tom/public_html ; chmod 755 /home/tom/public_html
```

More info. about userdir module:
[in french](https://fr.wikibooks.org/wiki/Apache/UserDir)



Once your server can be reached via `localhost/~usernamehere`,
then you can install PHP (the game has been tested using v7.1.33)\
along with basic PHP modules.

On ubuntu you can use the following command:

```
apt install php libapache2-mod-php php-mysql php-xml
```

It is strongly recommended to use symlinks between your virtual host
root e.g. `/var/www/html` and your `public_html` dir.
So the final URL for the game is:
`http://127.0.0.1/~tom/server/`

Finally, you need to allow PHP scripts to work from `public_html`,
to do this, edit the file
`/etc/apache2/mods-available/php8.0.conf`
for example.
Libraries used by the project are Propel as ORM,\
plus a [datto/php-json-rpc](https://github.com/datto/php-json-rpc) component...
To download composer and install libraries, change dir to `server/` then type:


```
$ wget http://getcomposer.org/composer.phar
# Or if you haven't wget on your computer
$ curl -s http://getcomposer.org/installer | php
# then
$ php composer.phar install
```




## Contribute / Contribuer

Feel free to contribute!\
Fork the project, use Pull Requests, or define new Issues.\
You can also join the Discord.

*Contribuez librement!*\
*Forkez le projet, utilisez des Pull Requests, ou déclarez de nouvelles Issues.*\
*Vous pouvez aussi rejoindre le Discord.*
