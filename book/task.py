from task9.celery import app
from django.contrib.auth.models import User
from .models import Reviews, Books
from django.core.mail import send_mass_mail


@app.task(name="send_weekly")
def send_weekly():
    emails = [x.email for x in User.objects.all()]
    books = Books.objects.all()
    
    high = 0

    for x in books:
        review = Reviews.objects.filter(book=x)

        if review:
            rat = [y.rating for y in review]
            avg = sum(rat)/len(rat)

            if avg>high:
                bk = x
                high = avg

    subject = "Weeekly Mail"
    message = f"{bk.title} is our recommendation for this week"
    email_from = "test@test.com"

    send_mass_mail((subject, message, email_from, emails), fail_silently=False)