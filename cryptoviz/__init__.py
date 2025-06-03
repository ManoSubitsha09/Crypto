from flask import Flask
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.models import load_model
def model_definition():
    model= Sequential()
    model.add(LSTM(256, return_sequences=True, input_shape=(1,1)))
    model.add(LSTM(256))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')

    return model

eth_model = model_definition()
eth_model.load_weights(r"C:\Users\Mano-PC\Downloads\crypto_final - Copy\cryptoforecast\webapp\cryptoviz\models\eth_model.h5")
#eth_model.predict(X_test)

btc_model = model_definition()
btc_model.load_weights(r"C:\Users\Mano-PC\Downloads\crypto_final - Copy\cryptoforecast\webapp\cryptoviz\models\btc_model.h5")
#btc_model.predict(X_test)

ltc_model = model_definition()
ltc_model.load_weights(r"C:\Users\Mano-PC\Downloads\crypto_final - Copy\cryptoforecast\webapp\cryptoviz\models\ltc_model.h5")
#ltc_model.predict(X_test)

xrp_model = model_definition()
xrp_model.load_weights(r"C:\Users\Mano-PC\Downloads\crypto_final - Copy\cryptoforecast\webapp\cryptoviz\models\xrp_model.h5")
#xrp_model.predict(X_test)

flaskapp = Flask(__name__)

import cryptoviz.views
