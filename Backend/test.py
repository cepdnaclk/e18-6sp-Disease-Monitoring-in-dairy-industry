import json 
from werkzeug.datastructures import FileStorage

try:
    from app import app
    import unittest

except Exception as e :
    print("Some modules are missing {}" .format(e))

class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = app.test_client()

    def test_predict_with_json_data(self):
        # Prepare a mock JSON request
        json_data = {
            'DIM( Days In Milk)': 100,
            'Avg(7 days). Daily MY( L )': 50,
            'Kg. milk 305 ( Kg )': 300,
            'Fat (%)': 3.5,
            'SNF (%)': 8.0,
            'Density ( Kg/ m3': 1020,
            'Protein (%)': 3.0,
            'Conductivity (mS/cm)': 15.0,
            'pH': 6.5,
            'Freezing point (⁰C)': -0.5,
            'Salt (%)': 0.1,
            'Lactose (%)': 4.5
        }

        response = self.client.get('/predict', json=json_data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Prediction" in data)
    
    def test_predict_without_json_data(self):
        response = self.client.get('/predict')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 500)
        self.assertTrue("error" in data)
        self.assertEqual(data["error"], "Request is not in JSON format")
    
    def test_predict_excel_with_valid_file(self):
        # Prepare a mock file upload
        with open("test_data.xlsx", "rb") as file:
            file_storage = FileStorage(file)
            response = self.client.get('/predict/excel', data={'excel_file': file_storage})

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Sample No" in data)
        self.assertTrue("Prediction" in data)
    
    def test_predict_excel_with_no_file(self):
        response = self.client.get('/predict/excel')

        self.assertEqual(response.status_code, 400)

if __name__ == "__main__" :
    unittest.main()