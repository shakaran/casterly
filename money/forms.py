from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _

from money.models import BankAccount, AVAILABLE_ENTITIES, MovementCategory, Movement
from money.parser import parse_csv, import_movements
from money.parser.banks import ENTITY_TO_PARSER


class UploadCSVstatementForm(forms.Form):
    estatement = forms.FileField()
    bank_account = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(UploadCSVstatementForm, self).__init__(*args, **kwargs)
        self.fields["bank_account"].choices = [
            (obj.pk, obj) for obj in BankAccount.objects.all()
        ]

    def save(self, *args, **kwargs):
        if self.is_valid():
            parser = ENTITY_TO_PARSER[BankAccount.objects.get(
                pk=self.cleaned_data['bank_account']).entity]
            data = parse_csv(
                self.cleaned_data["estatement"],
                parser=parser,
                header_lines=1,
                reverse_order=True,
            )

            bank_account = BankAccount.objects.get(
                pk=self.cleaned_data["bank_account"])
            import_movements(data, bank_account)


class InlineCategoryForm(forms.ModelForm):
    movement = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(InlineCategoryForm, self).__init__(*args, **kwargs)
        self.fields["movement"].widget = forms.widgets.HiddenInput()
        categories = [(None, _("None"))] + [
            (cat.id, cat) for cat in MovementCategory.objects.all()]

    class Meta:
        model = Movement
        fields = [
            "category",
        ]
