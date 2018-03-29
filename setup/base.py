from random import randint, shuffle

druzinky = [#
    'Muflóny',
]

veduci = [
    'Sára',
]

def create_password():
    big_letter = randint(1,4)
    digit = randint(1,5)
    small_letter = 10 - big_letter - digit
    password_list = []
    password = ''

    for i in range(big_letter):
        password_list.append(chr(randint(65,90)))

    for i in range(small_letter):
        password_list.append(chr(randint(97,122)))

    for i in range(digit):
        password_list.append(chr(randint(48,57)))

    shuffle(password_list)

    for s in password_list:
        password += s

    return password

with open('base_data.txt', 'w') as f:
    f.write("from django.contrib.auth.models import User\n")
    f.write("from obdlznik.models import *\n\n")

    for druzinka in druzinky:
        f.write("user = User.objects.create_user('%s', password='%s')\n" % (druzinka, create_password()))
        f.write("user.is_superuser=False\n")
        f.write("user.is_staff=False\n")
        f.write("user.save()\n")
        f.write("druzinka = Druzinka.objects.create(idUser=user, name='%s')\n" % (druzinka))
        f.write("Goal.objects.create(idDruzinka=druzinka, x=%d, y=%d)\n" % (randint(0,20), randint(0,20)))

    for veducko in veduci:
        f.write("user = User.objects.create_user('%s', password='%s')\n" % (veducko, create_password()))
        f.write("user.is_superuser=False\n")
        f.write("user.is_staff=True\n")
        f.write("user.save()\n")

    f.write("Message.objects.create(text='Databáza úspešne vytvorená!')\n")
    f.write("exit()")
