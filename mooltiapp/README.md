# Mooltiapp

Building

For Mac:

npm run build:osx

* Note: 

Permission error on MAC:

rm -Rf ~/.electron/
sudo npm install -g electron-prebuilt --unsafe-perm=true --allow-root

I also ran with problems building websocket, my solution was: inside app/node_modules/websocket/, edited package.json install script to "install": "node-gyp rebuild".

For Windows:

1) npm install -g electron-prebuilt 
2) npm install
3) delete the chrome_app file inside the app folder
4) copy the chrome app folder from the mooltipass root repository to the app folder
5) inside app/node_modules/websocket/, edited package.json install script to "install": "node-gyp rebuild".
6) npm run build:win