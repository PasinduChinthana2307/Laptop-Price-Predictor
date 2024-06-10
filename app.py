from flask import Flask ,render_template , request
import pickle
import numpy as np

app = Flask(__name__)

def prediction(lst):
    filename = 'model/Predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)

    pred_value = model.predict([lst])
    return pred_value



@app.route('/', methods =['POST','GET'])
def index():
    pred = 0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']
        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')
        
        feature_list = []
        feature_list.append(int(ram))
        feature_list.append(float(weight))
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))

        company_list = ['acer','apple','asus','dell','hp','lenovo','msi','other','toshiba']
        typename_list =['2in1convertiable','gaming','netbook','notebook','ultrabook','workstation']
        opsys_list = ['linux','mac','other','windows']
        cpu_list = ['amd','intelcorei3','intelcorei5','intelcorei7','other']
        gpu_list = ['amd','intel','nvidia']

        

        def traverse(lis,value):
            for item in lis:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)               

        traverse(company_list,company)
        traverse(typename_list,typename)
        traverse(opsys_list,opsys)
        traverse(cpu_list,cpu)
        traverse(gpu_list,gpu)

        pred = prediction(feature_list)
        pred = np.round(pred[0])
        


    return render_template('index.html', pred = pred)


if __name__ == '__main__':
    app.run(debug=True)