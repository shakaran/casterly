from django import forms

from money.models import BankAccount
from money.parser import parse_csv, import_movements
from money.parser.banks import AVAILABLE_ENTITIES, ENTITY_TO_PARSER


class UploadCSVstatementForm(forms.Form):
    estatement = forms.FileField()
    entity = forms.ChoiceField(choices=AVAILABLE_ENTITIES)
    bank_account = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(UploadCSVstatementForm, self).__init__(*args, **kwargs)
        self.fields["bank_account"].choices = [
            (obj.pk, obj) for obj in BankAccount.objects.all()
        ]

    def save(self, *args, **kwargs):
        if self.is_valid():
            parser = ENTITY_TO_PARSER[self.cleaned_data["entity"]]
            data = parse_csv(
                self.cleaned_data["estatement"],
                parser=parser,
                header_lines=1,
                reverse_order=True,
            )

            bank_account = BankAccount.objects.get(
                pk=self.cleaned_data["bank_account"])
            import_movements(data, bank_account)
