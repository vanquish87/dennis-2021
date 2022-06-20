from enum import unique
from django.db import models
import uuid
from users.models import Profile

# Create your models here.
class Project(models.Model):
    # many to one relationship 
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    # null=True: db can have null value, blank:True, it can be left blank in form
    description = models.TextField(null=True, blank=True)
    # image upload with a default image already if not uploaded
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    # many to many relationship with project
    # 'Tag' is used because it is declared after this Project class
    # if opposite was the cas then Tag should work instead of 'Tag'
    tags = models.ManyToManyField('Tag', blank=True)

    # to see how many votes & vote ratio are given for this project
    vote_total = models.IntegerField(default=0, null=True, blank=True) 
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)   
    # create Timestamp automatically
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # this is what you get when object is instantiated of this class
    # for ex: in Admin Panel
    def __str__(self):
        return self.title

    class Meta:
        # results display in which order
        # ordering : highest vote_ratio first, if there is tie than by highest vote_total
        ordering = ['-vote_ratio', '-vote_total']

    # to check if new reviewer has not already submitted a review
    # flat=True will give a list not object of ids
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset
    
    # @property will run this as 'attribute' not method to calculate vote
    # calculation on how many reviews on particular project
    @property
    def getVoteCount(self):
        # getting all reviews
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        # total votes
        totalVotes = reviews.count()
        # calculate this in % for usage
        ratio = (upVotes / totalVotes) * 100

        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


# one to many relationship
class Review(models.Model):
    # creating tuple for value that will be prefilled
    VOTE_TYPE = ( 
        ('up', 'Up Vote'),
        ('down', 'Down Vote')
    )
    # onetomany relationship
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    # to know what project this review is tied to
    # on_delete will decide if original Key ie, Project is deleted what will happen in this model, CASCADE will delete all the reviews
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    # 1 profile can leave 1 review per project
    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value

# many to many relationship with project
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.name