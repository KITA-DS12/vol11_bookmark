from controllers import app
import controllers

app.add_api_route('/', controllers.hello)
app.add_api_route('/upload', controllers.read_file, methods=['POST'])
