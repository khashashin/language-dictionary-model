from django.contrib.auth import get_user_model
from django.db import models


class BaseModel(models.Model):
    WORD_MODERATE_STATUS = [
        ('UNDER_CONCIDERATION', 'under consideration'),
        ('PREVIOUSLY_ACCEPTED', 'previously accepted')
    ]
    moderate_status = models.CharField(
        max_length=50, choices=WORD_MODERATE_STATUS, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(), related_name='%(class)s_createdby')
    modified_by = models.ForeignKey(
        get_user_model(), related_name='%(class)s_modifiedby', null=True, blank=True)
    acceppted = models.BooleanField(default=False)
    acceppted_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        related_name='%(class)s_acceptedby')
    word_category = models.ForeignKey(
        'CoreWordCategoryModel', on_delete=models.CASCADE,
        related_name='%(class)s_wordcategory')

    class Meta:
        abstract = True


class WordCoreModel(BaseModel):
    word_core = models.CharField(max_length=255, default="")
    word_russian_typed = models.CharField(max_length=255, default="", blank=True)
    word_english_typed = models.CharField(max_length=255, default="", blank=True)

    homonyms = models.ManyToManyField('self', blank=True)
    synonyms = models.ManyToManyField('self', blank=True)
    antonyms = models.ManyToManyField('self', blank=True)

    class Meta:
        indexes = [models.Index(fields=['word_core'])]
        verbose_name = 'Core Word'
        verbose_name_plural = 'Core Words'

    def __str__(self):
        return self.word_core


class MountainDialectVariant(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='akkish_dialects')
    dialect = models.CharField(max_length=255, default="")


class PlainDialectVariant(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='malkhish_dialects')
    dialect = models.CharField(max_length=255, default="")


class BorderDialectVariant(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='itum_qalish_dialects')
    dialect = models.CharField(max_length=255, default="")


class CoreWordPreffixModel(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='prefixes')
    order = models.SmallIntegerField()
    preffix = models.CharField(max_length=20)


class CoreWordSuffixModel(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='suffixes')
    order = models.SmallIntegerField()
    suffix = models.CharField(max_length=20)


class CoreWordEndingsModel(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='endings')
    order = models.SmallIntegerField()
    value = models.CharField(max_length=50, default="")


class CoreWordRootModel(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='roots')
    root = models.CharField(max_length=80)


class CoreWordSyllableModel(models.Model):
    '''
    This model represents each syllable of the word e.g.:
    bla-bla, bla-bla-bla-bla etc.
    '''
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='syllables')
    order = models.SmallIntegerField()
    syllable = models.CharField(max_length=50)


class CoreWordDescriptionModel(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='descriptions')
    description = models.TextField()


class CoreWordLatinVersionModel(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='latin_versions')
    latin_version = models.CharField(max_length=200)


class CoreWordTranscriptionModel(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='transcriptions')
    transcription = models.CharField(max_length=200)


class CoreWordIPAModel(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='ipas')
    ipa = models.CharField(max_length=200)


class CoreWordNounClassModel(models.Model):
    NOUN_CLASSESS = [
        ('V_CLASS', 'B class'),
        ('Y_CLASS', 'Y class'),
        ('Y_CLASS_SECOND', 'Y class II'),
        ('D_CLASS', 'D class'),
        ('B_CLASS', 'B class'),
        ('B_CLASS_SECOND', 'D class II')
    ]
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='noun_classes')
    word_class = models.CharField(max_length=20, choices=NOUN_CLASSESS)


class CoreWordCategoryModel(models.Model):
    ch_abbreviation = models.CharField(max_length=10)
    ch_description = models.CharField(max_length=50)
    ru_abbreviation = models.CharField(max_length=10)
    ru_description = models.CharField(max_length=50)
    en_abbreviation = models.CharField(max_length=10)
    en_description = models.CharField(max_length=50)


class CoreWordPartOfSpeechModel(models.Model):
    PART_OF_SPEECH = [
        ('NOUN', 'Noun'),
        ('VERB', 'Verb'),
        ('ADVERB', 'Adverb'),
        ('ADJECTIVE', 'Adjective'),
        ('PRONOUN', 'Pronoun'),
        ('PREPOSITION', 'Preposition'),
        ('CONJUNCTION', 'Conjunction'),
        ('INTERJECTION', 'Interjection')
    ]
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='part_of_speeches')
    part_of_speech = models.CharField(max_length=20, choices=PART_OF_SPEECH)


class CoreWordDeclensionSingularModel(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='declensions_singular')
    absolutive = models.CharField(max_length=255)
    genitive = models.CharField(max_length=255)
    dative = models.CharField(max_length=255)
    ergative = models.CharField(max_length=255)
    allative = models.CharField(max_length=255)
    instrumental = models.CharField(max_length=255)
    locative_stay = models.CharField(max_length=255)
    locative_direction = models.CharField(max_length=255)
    locative_outcome = models.CharField(max_length=255)
    locative_through = models.CharField(max_length=255)
    comparative = models.CharField(max_length=255)


class CoreWordDeclensionPluralModel(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='declensions_plural')
    absolutive = models.CharField(max_length=255)
    genitive = models.CharField(max_length=255)
    dative = models.CharField(max_length=255)
    ergative = models.CharField(max_length=255)
    allative = models.CharField(max_length=255)
    instrumental = models.CharField(max_length=255)
    locative_stay = models.CharField(max_length=255)
    locative_direction = models.CharField(max_length=255)
    locative_outcome = models.CharField(max_length=255)
    locative_through = models.CharField(max_length=255)
    comparative = models.CharField(max_length=255)


class CoreWordImperativeTense(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='imperative_tenses')
    basic_form = models.CharField(max_length=255)
    causative = models.CharField(max_length=255)
    permissive = models.CharField(max_length=255)
    permissive_causative = models.CharField(max_length=255)
    potential = models.CharField(max_length=255)
    inceptive = models.CharField(max_length=255)


class CoreWordSimplePresentTense(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='simple_present_tenses')
    basic_form = models.CharField(max_length=255)
    causative = models.CharField(max_length=255)
    permissive = models.CharField(max_length=255)
    permissive_causative = models.CharField(max_length=255)
    potential = models.CharField(max_length=255)
    inceptive = models.CharField(max_length=255)


class CoreWordNearPreteriteTense(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='near_preterite_tenses')
    basic_form = models.CharField(max_length=255)
    causative = models.CharField(max_length=255)
    permissive = models.CharField(max_length=255)
    permissive_causative = models.CharField(max_length=255)
    potential = models.CharField(max_length=255)
    inceptive = models.CharField(max_length=255)


class CoreWordWitnessedPastTense(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='witnessed_past_tenses')
    basic_form = models.CharField(max_length=255)
    causative = models.CharField(max_length=255)
    permissive = models.CharField(max_length=255)
    permissive_causative = models.CharField(max_length=255)
    potential = models.CharField(max_length=255)
    inceptive = models.CharField(max_length=255)


class CoreWordPerfectTense(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='perfect_tenses')
    basic_form = models.CharField(max_length=255)
    causative = models.CharField(max_length=255)
    permissive = models.CharField(max_length=255)
    permissive_causative = models.CharField(max_length=255)
    potential = models.CharField(max_length=255)
    inceptive = models.CharField(max_length=255)


class CoreWordPlusquamperfectTense(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='plusquamperfect_tenses')
    basic_form = models.CharField(max_length=255)
    causative = models.CharField(max_length=255)
    permissive = models.CharField(max_length=255)
    permissive_causative = models.CharField(max_length=255)
    potential = models.CharField(max_length=255)
    inceptive = models.CharField(max_length=255)


class CoreWordRepeatedPastTense(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='repeated_past_tenses')
    basic_form = models.CharField(max_length=255)
    causative = models.CharField(max_length=255)
    permissive = models.CharField(max_length=255)
    permissive_causative = models.CharField(max_length=255)
    potential = models.CharField(max_length=255)
    inceptive = models.CharField(max_length=255)


class CoreWordPossibleFutureTense(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='possible_future_tenses')
    basic_form = models.CharField(max_length=255)
    causative = models.CharField(max_length=255)
    permissive = models.CharField(max_length=255)
    permissive_causative = models.CharField(max_length=255)
    potential = models.CharField(max_length=255)
    inceptive = models.CharField(max_length=255)


class CoreWordRealFutureTense(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='real_future_tenses')
    basic_form = models.CharField(max_length=255)
    causative = models.CharField(max_length=255)
    permissive = models.CharField(max_length=255)
    permissive_causative = models.CharField(max_length=255)
    potential = models.CharField(max_length=255)
    inceptive = models.CharField(max_length=255)


class CoreWordEtymologyModel(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='etimologies')
    etymology = models.TextField()


class CoreWordPhraseologismsAndSustainableCombinationsModel(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='phraseologisms')
    definition = models.TextField()


class CoreWordSourceModel(models.Model):
    word = models.ForeignKey(
        WordCoreModel, on_delete=models.CASCADE,
        related_name='sources')
    source = models.CharField(max_length=255)
