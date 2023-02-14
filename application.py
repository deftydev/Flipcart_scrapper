from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

application=Flask(__name__)

@application.route("/",methods=['GET'])
def homepage():
    return render_template('index.html')

@application.route("/review",methods=['GET','POST'])
def Review():
    if request.method=='POST':
        try:
            content=request.form['content']
            flipcart_url= "https://www.flipkart.com/search?q=" + content 
            uclient = uReq(flipcart_url) 
            flipcart_page = uclient.read() 
            flipcart_html = bs(flipcart_page, "html.parser")
            bigboxes= flipcart_html.find_all("div",{"class":"_1AtVbE col-12-12"})
            product_original_link = bigboxes[2].div.div.div.a['href']
            product_link= "https://www.flipkart.com"+ product_original_link
            product_req= requests.get(product_link) 
            product_req.encoding='utf-8'
            product_html= bs(product_req.text, "html.parser") 
            comment_box= product_html.find_all("div",{"class":"_16PBlm"})
            reviews=[]
            for i in comment_box:
                try:
                    rating= i.div.div.div.div.text
                except:
                    rating = "3"
                try:
                    user = i.div.div.find("p",{"class":"_2-N8zT"}).text
                except:
                    user= "Anonymous"
                try:
                    commented =i.div.div.find("div",{"class":""}).text
                except:
                    commented= "hidden"
                my_dict = {"product":content , "name":user , "rating":rating , "comment":commented}
                reviews.append(my_dict)
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
        
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__=="__main__":
    application.run(host="0.0.0.0")


            