import pandas as pd
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import UploadFileForm

def handle_uploaded_file(f):
    df = pd.read_excel(f)
    summary = df.groupby('Cust State')['DPD'].sum().reset_index()
    return summary

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            summary = handle_uploaded_file(request.FILES['file'])
            summary_text = summary.to_string(index=False)

            if request.user.is_authenticated:
                full_name = request.user.get_full_name()
            else:
                full_name = "Kunal Arya"

            send_mail(
                subject=f'Python Assignment - {full_name}',
                message=summary_text,
                from_email='kunalarya88779@gmail.com',
                recipient_list=['kunalarya873@gmail.com'],
                fail_silently=False,
            )

            return render(request, 'uploader/success.html', {'summary': summary_text})

    else:
        form = UploadFileForm()

    return render(request, 'uploader/upload.html', {'form': form})
