from django.shortcuts import HttpResponse


from django.conf import settings

from django.shortcuts import render
from .models import Blog
import PyPDF2
from transformers import pipeline
from googletrans import Translator

def extract_pdf_to_db(request):
    
    if request.method == 'POST':
        # Check if the form has passed a file
        pdf_file = request.FILES.get('pdf_file')
        if pdf_file and pdf_file.name.endswith('.pdf'):
            # Save the PDF to a temporary file or read directly from memory
            doc = PyPDF2.PdfReader(pdf_file)

            all_text = ""
            for page in doc.pages:
                txt = page.extract_text()
                if txt:
                    all_text += txt + "\n"
            
            # Check if the document has at least one page
            if len(doc.pages) > 0:
                first_page = doc.pages[0]
                text = first_page.extract_text()

                translator = Translator()

                if text:
                    # Initialize the summarization pipeline
                    summarizer = pipeline("summarization")

                    # Generate summary for the first page text
                    initial_summary = summarizer(text, max_length=300, min_length=50, do_sample=False)[0]['summary_text']

                    # Define your ideal maximum length and find the last period before exceeding it
                    max_length = 200
                    if len(initial_summary) > max_length:
                        # Find the last period within the max length range
                        last_period_index = initial_summary.rfind('.', 0, max_length)
                        if last_period_index == -1:
                            # If no period found, use the first period after the max length (if any)
                            last_period_index = initial_summary.find('.', max_length)
                        titre = initial_summary[:last_period_index + 1] if last_period_index != -1 else initial_summary
                    else:
                        titre = initial_summary

                    titre_fr = translator.translate(titre, src='en', dest='fr').text
                    print(titre_fr)
                else:
                    print("No text found on the first page.")
            else:
                print("Document is empty.")

            
            full_summary = summarizer(text, max_length=500, min_length=100, do_sample=False)[0]['summary_text']
            full_summary_fr = translator.translate(full_summary, src='en', dest='fr').text
            print(full_summary_fr)

            import dateutil.parser as dparser

            def transform_dates(text):
                # Words that potentially could be part of date expressions
                date_keywords = ('Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet',
                'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre',
                'Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun',
                'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc',
                'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche',
                'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim',
                '/', '-', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0')


                words = text.split()
                temp_date = []
                for word in words:
                    if any(keyword in word for keyword in date_keywords):
                        temp_date.append(word)
                    else:
                        if temp_date:
                            # Join the collected date parts and try to parse it
                            date_str = ' '.join(temp_date)
                            try:
                                parsed_date = dparser.parse(date_str, fuzzy=True)
                                return parsed_date.strftime('%Y-%m-%d')  # Return the first successfully parsed date
                            except ValueError:
                                pass
                            temp_date = []

                # Handle the last potential date
                if temp_date:
                    date_str = ' '.join(temp_date)
                    try:
                        parsed_date = dparser.parse(date_str, fuzzy=True)
                        return parsed_date.strftime('%Y-%m-%d')
                    except ValueError:
                        pass

                return None  # Return None if no dates were found

            first_date = transform_dates(text)
            print(first_date)
            print(full_summary)

            Blog.objects.create(title=titre_fr,description=all_text,publish=first_date,summary=full_summary_fr,uploaded_file=pdf_file)


            return render(request, "afterPdf.html")
        else:
            return HttpResponse("Invalid file format. Please upload a PDF file.")

    # For GET requests, just render the upload form.
    return render(request, 'pdf.html')


import cv2
import matplotlib.pyplot as plt
import pytesseract


import numpy as np
def extract_ocr(request):

    pytesseract.pytesseract.tesseract_cmd = r'C:\Apache24\htdocs\venv\tesseract.exe'



    if request.method == 'POST' and request.FILES['image_file']:
        # Read the uploaded image file
        image_file = request.FILES['image_file']

        img = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        



        def display(im_data):
            dpi = 80
            height, width = im_data.shape[:2]
            figsize = width / float(dpi), height / float(dpi)
            fig = plt.figure(figsize=figsize)
            ax = fig.add_axes([0, 0, 1, 1])
            ax.axis('off')
            ax.imshow(im_data, cmap='gray')
            plt.show()

        def grayscale(image_file):
            return cv2.cvtColor(image_file, cv2.COLOR_BGR2GRAY)

        gray_img = grayscale(img)

        thresh, im_bw = cv2.threshold(gray_img, 210, 230, cv2.THRESH_BINARY)

        def noise_removal(image):
            import numpy as np
            kernel = np.ones((1, 1), np.uint8)
            image = cv2.dilate(image, kernel, iterations=1)
            kernel = np.ones((1, 1), np.uint8)
            image = cv2.erode(image, kernel, iterations=1)
            image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
            image = cv2.medianBlur(image, 3)
            return image
        
        
        ocr_result = pytesseract.image_to_string(im_bw)
        print(ocr_result)

        no_noise = noise_removal(im_bw)
        
        translator = Translator()
        if ocr_result:
                # Initialize the summarization pipeline
                summarizer = pipeline("summarization")

                # Generate summary for the first page text
                initial_summary = summarizer(ocr_result, max_length=300, min_length=50, do_sample=False)[0]['summary_text']

                # Define your ideal maximum length and find the last period before exceeding it
                max_length = 200
                if len(initial_summary) > max_length:
                    # Find the last period within the max length range
                    last_period_index = initial_summary.rfind('.', 0, max_length)
                    if last_period_index == -1:
                        # If no period found, use the first period after the max length (if any)
                        last_period_index = initial_summary.find('.', max_length)
                    titre = initial_summary[:last_period_index + 1] if last_period_index != -1 else initial_summary
                else:
                    titre = initial_summary

                
                titre_fr = translator.translate(titre, src='en', dest='fr').text
                print(titre_fr)

        
        full_summary = summarizer(ocr_result, max_length=500, min_length=100, do_sample=False)[0]['summary_text']
        full_summary_fr = translator.translate(full_summary, src='en', dest='fr').text
        #print()

        import dateutil.parser as dparser

        def transform_dates(text):
            # Words that potentially could be part of date expressions
            date_keywords = ('Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet',
                'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre',
                'Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun',
                'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc',
                'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche',
                'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim',
                '/', '-', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0')

            words = text.split()
            temp_date = []
            for word in words:
                if any(keyword in word for keyword in date_keywords):
                    temp_date.append(word)
                else:
                    if temp_date:
                        # Join the collected date parts and try to parse it
                        date_str = ' '.join(temp_date)
                        try:
                            parsed_date = dparser.parse(date_str, fuzzy=True)
                            return parsed_date.strftime('%Y-%m-%d')  # Return the first successfully parsed date
                        except ValueError:
                            pass
                        temp_date = []

            # Handle the last potential date
            if temp_date:
                date_str = ' '.join(temp_date)
                try:
                    parsed_date = dparser.parse(date_str, fuzzy=True)
                    return parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    pass

            return None  # Return None if no dates were found

        first_date = transform_dates(ocr_result)
        print(first_date)
        print(full_summary)

        Blog.objects.create(title=titre_fr,description=ocr_result,publish=first_date,summary=full_summary_fr,image=image_file)

    
        return render(request, 'afterOCR.html')
    else:
        return render(request,"OCR.html")

    
        
    


def blog_archive(request):
    # Assuming `publish` is the field with the publication date
    latest_blogs = Blog.objects.all().order_by('-publish')[:5]
    context = {
        'latest_blogs': latest_blogs
    }
    return render(request, 'blog_detail.html', context)



def afterPdf(request):
    return render(request, 'afterPdf.html')

from django.shortcuts import render, get_object_or_404

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})

def contact(request):
    return render(request, 'contactUs.html')

def about(request):
    return render(request, 'about.html')

def pdf(request):
    return render(request, 'pdf.html')


