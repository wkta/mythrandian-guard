# Mythrandian Guard

<center>
<a href="https://discord.gg/24DfrtvpXk"><img src="discord-logo.png" height="48"></a>
</center>

A game of Heroes and Lackeys\
*Un jeu de Héros et de Laquais*

## Development: client-side


## Development: server-side

(Proof-tested using Ubuntu 21.10, should work with any Linux system)

First install software for running http servers:
apache and mysql... Using a firewall is strongly recommanded.

```
$ sudo apt install apache2
$ sudo apt install mysql-server  # or mariadb-server mariadb-client
```
remember you may need to open `public_html` on read, example:
```
a2enmod userdir
chmod 755 /home/tom
mkdir /home/tom/public_html ; chmod 755 /home/tom/public_html
```

More info.
[in french](https://fr.wikibooks.org/wiki/Apache/UserDir)

Once your server can be reached via `localhost/~usernamehere`,
then you can install PHP (the game has been tested using v7.1.33)\
On ubuntu you can use:

```
apt-get install php 
# for old systems: install php7.4-common php7.4-mysql libapache2-mod-php7.4
```

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


## Chosen tech stack (overview)

Python and the katagames SDK on the client-side,\
PHP on the server-side.\

*Python et le SDK katagames côté client,*\
*PHP sur le côté serveur.*\


## Type of game / Type de jeu

Idle-game + "Deck building" game


## Gameplay overview / Aperçu du gameplay

You start with a hero, you collect new gear and new Lackeys by picking up missions. A selected mission needs to be hard enough so your rewards are worthy, but not too hard otherwise your hero/team is wounded and you loose some time generally speaking (->no progress made).

*Tu démarres avec un héros, tu collectionnes du nouveau matériel et de nouveaux Laquais via la sélection de missions. Une mission sélectionnée doit être suffisament difficile de manière à produire des récompenses de valeur, mais pas trop difficile autrement ton héros/équipe est blessée et tu perds du temps de manière générale (->absence de progression).*


## Contribute / Contribuer

Feel free to contribute!\
Fork the project, use Pull Requests, or define new Issues.\
You can also join the Discord.

*Contribuez librement!*\
*Forkez le projet, utilisez des Pull Requests, ou déclarez de nouvelles Issues.*\
*Vous pouvez aussi rejoindre le Discord.*
