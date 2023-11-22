from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load the pre-trained decision tree model
model = joblib.load('model.pkl')

def convert_categorical(value):
    jenis_kelamin_mapping = {'Laki - Laki': 0, 'Perempuan': 1}
    aktif_sosial_media_mapping = {'Ya': 1, 'Tidak': 0}
    durasi_sosmed_mapping = {'1 - 4 jam': 0, '4 - 8 jam': 1, '> 8 jam': 2}
    kecemasan_mapping = {'Ya': 1, 'Tidak': 0}
    aktivitas_fisik_mapping = {'Ya': 1, 'Tidak': 0}

    # Use the provided mapping to convert categorical value to numeric
    if 'Jenis Kelamin' in value:
        return jenis_kelamin_mapping.get(value['Jenis Kelamin'], None)
    elif 'Aktif Sosial Media' in value:
        return aktif_sosial_media_mapping.get(value['Aktif Sosial Media'], None)
    elif 'Durasi Sosmed' in value:
        return durasi_sosmed_mapping.get(value['Durasi Sosmed'], None)
    elif 'Kecemasan Terhadap Konten Medsos' in value:
        return kecemasan_mapping.get(value['Kecemasan Terhadap Konten Medsos'], None)
    elif 'Aktifitas Fisik Mengurangi Stress' in value:
        return aktivitas_fisik_mapping.get(value['Aktifitas Fisik Mengurangi Stress'], None)
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user input from the form
        umur = request.form['Umur']
        jenis_kelamin = request.form['JenisKelamin']
        # AktifSosialMedia = request.form['AktifSosialMedia']
        # DurasiSosmed = request.form['DurasiSosmed']
        # TingkatKebergunaanKonten = request.form['TingkatKebergunaanKonten']
        # TingkatKebahagiaan = request.form['TingkatKebahagiaan']
        # KecemasanTerhadapKontenMedsos = request.form['KecemasanTerhadapKontenMedsos']
        # AktifitasFisikMengurangiStress = request.form['AktifitasFisikMengurangiStress']
        DurasiTidur = request.form['DurasiTidur']
        DurasiTanpaMedsos = request.form['DurasiTanpaMedsos']
        
        # Convert categorical data to numeric
        input_data = {
        'Durasi Tidur': int(DurasiTidur),
        'Jenis Kelamin': convert_categorical({'Jenis Kelamin': jenis_kelamin}),
        'Durasi Tanpa Medsos': int(DurasiTanpaMedsos),
        'Umur': int(umur),
        # 'Aktif Sosial Media': convert_categorical({'Aktif Sosial Media': AktifSosialMedia}),
        # 'Durasi Sosmed': convert_categorical({'Durasi Sosmed': DurasiSosmed}),
        # 'Pengaruh Konten Medsos Untuk Hidup': int(TingkatKebergunaanKonten), 
        # 'Tingkat Kebahagiaan Aktif Medsos': int(TingkatKebahagiaan), 
        # 'Kecemasan Terhadap Konten Medsos': convert_categorical({'Kecemasan Terhadap Konten Medsos': KecemasanTerhadapKontenMedsos}),
        # 'Aktifitas Fisik Mengurangi Stress': convert_categorical({'Aktifitas Fisik Mengurangi Stress': AktifitasFisikMengurangiStress}),
        }


        # Reshape the input data to match the format expected by the model
        input_data_reshaped = pd.DataFrame([input_data])

        # Use the model to make a prediction
        prediction = model.predict(input_data_reshaped)
      
        
        # Use the model to make a prediction
        
        # Pass the prediction result to the HTML template
        return render_template("index.html", prediction_text="{}".format(prediction))

    # Render the initial HTML form
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
