from django.db import models

from accounts.models import Users

class Company(models.Model):
    name = models.CharField(max_length=300)
    about_company = models.CharField(max_length=2000)
    picture = models.ImageField(upload_to='company_pictures')
    read_more = models.CharField(max_length=2000, default='')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'about_company': self.about_company,
            'read_more':self.read_more,
            'picture': self.picture
        }


class JobCategory(models.Model):
    title = models.CharField(max_length=300)


class Opportunity(models.Model):
    title = models.CharField(max_length=300)
    job_type = models.CharField(max_length=300)
    description = models.CharField(max_length=2000)
    key_benefits = models.CharField(max_length=2000)
    deadline = models.CharField(max_length=300)
    requirements = models.CharField(max_length=300)
    read_more_link = models.CharField(max_length=300)
    apply_link = models.CharField(max_length=300)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='opportunities')
    location = models.CharField(max_length=300, default='')
    contract_type = models.CharField(max_length=300, default='')
    job_category = models.ForeignKey(JobCategory, null=True, on_delete=models.SET_NULL, default=None)


class Subscription(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Favourate(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


