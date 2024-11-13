import unittest
from models.text_generation import TextGenerator

class TestTextGeneration(unittest.TestCase):

    def setUp(self):
        # Initialize the TextGenerator with a dummy API key
        self.text_generator = TextGenerator(api_key='AIzaSyCsas4FZb-kFf8IIBVMtCbvEguClTP0ktw')

    def test_generate_response(self):
        emotion_state = "sad"
        user_input = "Hello, how are you?"
        personality = "angry"
        
        response = self.text_generator.generate_response(emotion_state, user_input, personality)
        print(response)
        
        # self.assertEqual(response)

if __name__ == '__main__':
    unittest.main()
