import os
import subprocess


'''
    composer identity issue -c admin@one-network -f mikeleow.card -u mikeleow -a "resource:org.acme.model.owner#owner01"
    composer card import -f mikeleow.card
    sed -e 's/localhost:/orderer.example.com:/' -e 's/localhost:/peer0.org1.example.com:/' -e 's/localhost:/peer0.org1.example.com:/' -e 's/localhost:/ca.org1.example.com:/' < $HOME/.composer/cards/mikeleow@one-network/connection.json > /tmp/connection.json && cp -p /tmp/connection.json $HOME/.composer/cards/mikeleow@one-network
    composer card export -f mikeleow_exp.card -c mikeleow@one-network ; rm mikeleow.card
'''
prompt ='composer card list'
subprocess.call(prompt)