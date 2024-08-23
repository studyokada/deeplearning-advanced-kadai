from .forms import ImageUploadForm
from django.shortcuts import render
from django.conf import settings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import decode_predictions


from io import BytesIO
import os




def predict(request):
    if request.method == 'GET':
        # GETリクエストによるアクセス時の処理を記述
        form = ImageUploadForm()
        return render(request, 'home.html', {'form': form})
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_file = form.cleaned_data["image"]
            img_file = BytesIO(img_file.read())
            img = load_img(img_file, target_size=(224, 224))
            img_array = img_to_array(img)
            img_array = img_array.reshape((1, 224, 224, 3))
            img_array = preprocess_input(img_array)
            model_path = os.path.join(settings.BASE_DIR, 'prediction', 'models', 'vgg16.h5')
            model = load_model(model_path)
            result = model.predict(img_array)
            result = decode_predictions(result)
            result_dict = {}
            for sublist in result:
                for tuple_item in sublist:
                    result_dict[tuple_item[1]] = tuple_item[2]*100
            
            img_data = request.POST.get("img_data")
            prediction = result_dict
            str = list(prediction)
            print(str[0])
            return render(request, "home.html", {"form": form, "prediction": prediction, "img_data": img_data})
        else:
            form = ImageUploadForm()
            return render(request, "home.html", {"form": form})
    