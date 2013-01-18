from django.db import models
from django_extensions.db.fields import UUIDField


"""
Short UUID-Doku:
http://david.feinzeig.com/blog/2012/03/01/how-to-add-a-uuid-field-in-django-using-django-extensions-and-how-to-make-it-a-read-only-admin-field/
"""


class Identity(models.Model):
    uuid = UUIDField(primary_key=True, version=4)
    ctime = models.DateTimeField('created', auto_now_add=True, blank=False)
    mtime = models.DateTimeField('modified', auto_now=True, blank=False)
    comment = models.TextField(default="", blank=True)

    class Meta:
        abstract = True


class MicroscopeInfo(models.Model):
    zoom = models.DecimalField(max_digits=5, decimal_places=2)
    lense = models.DecimalField(max_digits=5, decimal_places=2)
    gain = models.DecimalField(max_digits=5, decimal_places=2)
    laser_color = models.CharField(max_length=64)
    laser_config = models.CharField('e.g. gain/time/percentage', max_length=64)
    voxel_size_x = models.DecimalField('voxel x-size in nm', max_digits=7, decimal_places=2)
    voxel_size_y = models.DecimalField('voxel y-size in nm', max_digits=7, decimal_places=2)


    class Meta:
        abstract = True


class FileFolder(Identity):
    checksum = models.CharField(max_length=64)


class Experimenter(Identity):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True)
    title = models.CharField(max_length=16)
    affiliations = models.CharField(max_length=128)

    def __unicode__(self):
        return self.fullname

    @property
    def fullname(self):
        return u"%s %s %s" % (self.title, self.first_name, self.last_name)


class Experiment(Identity):
    label = models.CharField(unique=True, max_length=64)
    date = models.DateField()
    experimenter = models.ForeignKey(Experimenter)
    lab_book_entry = models.TextField()

    def __unicode__(self):
        return self.label


class AnimalType(Identity):
    notation = models.CharField(unique=True, max_length=64)

    def __unicode__(self):
        return self.notation


class Animal(Identity):
    label = models.CharField(unique=True, max_length=64)
    experiment = models.ForeignKey(Experiment)
    animal_type = models.ForeignKey(AnimalType)
    age = models.BigIntegerField("age in days [P]") #age in days
    age_uncertainty = models.CharField(max_length=64, blank=True)
    species = models.CharField(max_length=64)


    def __unicode__(self):
        return self.label


class MicroscopeSlide(Identity):
    label = models.CharField(unique=True, max_length=64)
    animal = models.ForeignKey(Animal)

    def __unicode__(self):
        return self.label


class NeuronType(Identity):
    type = models.CharField(unique=True, max_length=64)


class Neuron(Identity):
    label = models.CharField(unique=True, max_length=64)
    type = models.ForeignKey(NeuronType)
    microscope_slide = models.ForeignKey(MicroscopeSlide)

    def __unicode__(self):
        return self.label


class ImageStack(Identity, MicroscopeInfo):
    label = models.CharField(max_length=64)
    microscope_slide = models.ForeignKey(MicroscopeSlide)
    file_folder = models.ForeignKey(FileFolder)
    voxel_size_z = models.DecimalField('voxel z-size in nm', max_digits=7, decimal_places=2)


class Image(Identity, MicroscopeInfo):
    microscope_slide = models.ForeignKey(MicroscopeSlide)
    file_folder = models.ForeignKey(FileFolder)


class Morphology(Identity):
    dye = models.CharField(max_length=64)
    experimental_method = models.TextField()
    reconstruction_method = models.TextField()
    neuron = models.ForeignKey(Neuron)
    file_folder = models.ForeignKey(FileFolder)


