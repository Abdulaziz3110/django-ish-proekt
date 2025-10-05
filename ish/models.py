from django.db import models

# Xodimlar jadvali
class Xodim(models.Model):
    ism = models.CharField(max_length=100)
    familiya = models.CharField(max_length=100)
    bolim = models.CharField(max_length=100, blank=True, null=True)
    lavozim = models.CharField(max_length=100, blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, null=True)
    ish_haqi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ishga_kirilgan_sana = models.DateField(blank=True, null=True)

    def umumiy_maosh(self):
        # Xodimning ish kunlari orqali umumiy maoshni hisoblash
        ishlar = IshKuni.objects.filter(xodim=self)
        summa = sum(i.mahsulot.narxi * i.soni for i in ishlar)
        return summa

    def __str__(self):
        return f"{self.ism} {self.familiya}"


# Mahsulotlar jadvali
class Mahsulot(models.Model):
    nomi = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    narxi = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nomi} ({self.model})"


# Ish kuni jadvali
class IshKuni(models.Model):
    xodim = models.ForeignKey(Xodim, on_delete=models.CASCADE)
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE)
    sana = models.DateField()
    soni = models.IntegerField(default=0)  # nechta mahsulot tikdi

    def __str__(self):
        return f"{self.xodim} - {self.mahsulot} - {self.sana}"
