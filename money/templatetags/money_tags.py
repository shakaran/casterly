from django import template

from money.forms import InlineCategoryForm

register = template.Library()


@register.inclusion_tag("money/category_inline.html")
def inline_edit(category, movement):
    form = InlineCategoryForm({
        "category": category,
        "movement": movement.pk}, instance=movement)

    return {"form": form}
