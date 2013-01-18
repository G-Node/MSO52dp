__author__ = 'philipp'

from django.contrib import admin
from data_manager.models import Neuron, Experiment, Experimenter, Animal, MicroscopeSlide


class NeuronInline(admin.StackedInline):
    fields = ['label', 'type', 'microscope_slide']
    model = Neuron
    extra = 0


class MicroscopeSlideInline(admin.TabularInline):
    fields = ['label', 'animal']


class AnimalInline(admin.TabularInline):
    fields = ['label', 'species', 'age', 'age_uncertainty']
    model = Animal
    extra = 0
    inlines = [MicroscopeSlideInline]



class MicroscopeSlideAdmin(admin.ModelAdmin):
    fields = ['label', 'animal']
    inlines = [NeuronInline]


class AnimalAdmin(admin.ModelAdmin):
    fields = ['label', 'species', 'age', 'age_uncertainty']
    inlines = [MicroscopeSlideInline]


class ExperimenterAdmin(admin.ModelAdmin):
    fields = ['title', 'last_name', 'first_name', 'middle_name', 'affiliations', 'comment']
    list_display = ('fullname', 'affiliations', 'ctime', 'mtime')


class ExperimentAdmin(admin.ModelAdmin):
    fields = ['label', 'experimenter', 'date', 'lab_book_entry', 'comment']
    list_display = ('label', 'date', 'experimenter')
    inlines = [AnimalInline]



admin.site.register(Experimenter, ExperimenterAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(MicroscopeSlide, MicroscopeSlideAdmin)
admin.site.register(Neuron)
#admin.site.register(Animal, AnimalAdmin)

