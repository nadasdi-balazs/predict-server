# from flask import Flask, jsonify, request
# import traceback
#
# app = Flask("app")

class AzhuEmailClassifier:
    import os
    import bs4 as bs
    import re
    import langdetect
    import joblib
    import langdetect

    def __init__(self):
        pass

    def prettify(self,raw_string):
        try:
            raw_text = raw_string.replace("\n","")
            soup= self.bs.BeautifulSoup(raw_text)
            clean = soup.get_text()
            return clean
        except:
            pass
        else:
            return ""


    def detect_language(self, raw_string):
        try:
            language=self.langdetect.detect(raw_string)
        except:
            language='hu'
        return language

    def extract_subject(self, raw_string):

        my_string=raw_string

        if my_string.find("Feladó")>=0:
            try:
                email_subject= self.re.search(r'Tárgy:(.*?)<br',my_string).group(1)
            except:

                email_subject= ""
        else:
            email_subject= ""

        return email_subject


    def body_separator(self, raw_string):
        my_string = raw_string.replace("\n","")
        substring_1 = r'<html><head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-2"><meta name="Generator" content="Microsoft Exchange Server">'
        substring_2 = r'<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">'
        substring_3 = r'<html><body><p style="margin:0">'
        substring_4 = r'<html xmlns:v="urn:schemas-microsoft-com:vml"'
        substring_5= r'<html dir="ltr"><head>'
        substring_6 = r'Internetes honlapunkról az alábbi megkeresés érkezett'

        if my_string.startswith(substring_1):
            body= self.re.search(r'(?<=Tárgy:).*',my_string).group(0)
            email_body= self.re.search(r'(<br).*',body).group(0)
            clean_body = self.prettify(email_body)
            return clean_body

        elif my_string.startswith(substring_2) and my_string.find(r'<meta name="Generator" content="Microsoft Exchange Server">')<0:
            clean_body = self.prettify(my_string)
            return clean_body

        elif my_string.startswith(substring_3) and my_string.find(r'<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-2">')>=0:
            body= self.re.search(r'(?<=Tárgy:).*',my_string).group(0)
            email_body= self.re.search(r'(<br).*',body).group(0)
            clean_body = self.prettify(email_body)
            return clean_body

        elif my_string.startswith(substring_3) or my_string.startswith(substring_4) or my_string.startswith(substring_5):
            separator=r'<meta http-equiv="Content-Type" content="text/html; charset=utf-8">'
            result_list=my_string.split(separator)

            if len(result_list)>=2:
                return result_list[1]
            else:
                my_string=value
                separator=r'<div class="WordSection1">'
                result_list=my_string.split(separator)
                if len(result_list)>=2:
                    return result_list[1]
                else:
                    return np.nan


        else:
            return my_string



    def retrain_model(self, csv_file):
        '''
        This function retrains the model based on the uploaded csv file. The csv file
        must be named "retrain_data.csv" and most have two columns. The first column
        must contain the text of the email, the second column must contain the
        assigned category. The file must not have any headers.
        '''

        pass


    def clean_body(self,raw_string):
        cleaned_body_string = self.body_separator(raw_string)
        return cleaned_body_string

    def clean_subject_n_body(self,raw_string):
        body_string = self.body_separator(raw_string)
        subject = self.extract_subject(raw_string)
        cleaned_body_string = self.prettify(body_string)
        result = subject + " " + cleaned_body_string
        return result

    def detect_language(self, raw_string):
        try:
            language = langdetect.detect(raw_string)
        except:
            print("-- ERROR occurred during language detecion, will default to Hungarian")
            language = 'hu'
        return language

    def predict(self,raw_string):
        cleaned_string = self.clean_subject_n_body(raw_string)

        self.os.chdir(r"c:\balazs_cuccai\dev\azhu_deployment") # <---- a modell mappaja

        model_filename="azhu_emailclassifier.sav"
        clf = self.joblib.load(model_filename)

        language = self.detect_language(cleaned_string)
        if language =='de':
            print("-- German letter received")
            return 'CC_NEMET_LEVELEK'
        elif language != 'hu':
            print("-- Other non-Hungarian letter received")
            return 'CC_ANGOL_ES_EGYEB_NYELVU_LEVELEK'

        prediction = clf.predict([cleaned_string])
        result = str(prediction[0])
        return result




#     @app.route('/predict', methods=['POST'])
#     def predict_endpoint(self):
#         try:
#             json = request.get_json()
#             print("-- will predict, incoming json: '" + str(json) + "'")
#             temp=list(["0",json["content"]])
#             print("-- will predict, original input: '" + temp + "'")
#             prediction = self.predict(temp)
#             return jsonify({'prediction': str(prediction[0])})
#         except:
#             print("-- ERROR occurred")
#             return jsonify({'trace': traceback.format_exc()})
#
#
# if __name__ == '__main__':
#     app.run(debug=True)