from flask import Flask
from flask_restful import Resource, Api
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.externals import joblib
from flask_restful import reqparse
import pandas as pd
import json
class ItemSelector(BaseEstimator, TransformerMixin):
    """
    Parameters
    ----------
    key : hashable, required
        The key corresponding to the desired value in a mappable.
    """
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict[self.key]
    
    def inverse_transform(self, X):
        return X
clf = joblib.load('model/modelAD.pkl') 
app = Flask(__name__)
api = Api(app)
class predict(Resource):
    def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('MRUN', type=int, help='RUT codificado del alumno')
		parser.add_argument('SOBRE_EDAD_ALU', type=float, help='Edad que tiene el alumno en base al esperado del curso')
		parser.add_argument('PROM_GRAL_RANK', type=float, help='Ranking del promedio general en el curso')
		parser.add_argument('ASISTENCIA_RANK', type=float, help='Ranking de la asistencia en el curso')
		parser.add_argument('EDU_SUP_P', type=bool, help='1 si el padre tiene educacion superior completa o 0 en caso contrario')
		parser.add_argument('EDU_SUP_M', type=bool, help='1 si la madre tiene educacion superior completa o 0 en caso contrario')
		parser.add_argument('ING_HOGAR', type=int, help='Ingreso del hogar del 0 a 12')
		parser.add_argument('GSE_MANZANA_RBD', type=int, help='GSE de la manzana del establecimiento 1 2 3')
		parser.add_argument('GSE_MANZANA_ALU', type=int, help='GSE de la manzana de la residencia del alumno 1 2 3')
		parser.add_argument('SELECCION_RBD', type=bool, help='Si el establecimiento selecciona a los alumnos mediante un examen inicial')
		params = parser.parse_args()
		df = pd.DataFrame([params])
		pred = clf.predict(df.drop('MRUN',1))
		print(pred)
		return {'MRUN' : params['MRUN'],'DESERTA_ALU' : pred[0] }
api.add_resource(predict, '/predict', endpoint='bar')

if __name__ == '__main__':
    app.run(debug=True)