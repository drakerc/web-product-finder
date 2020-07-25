from django.db import models


class Brand(models.Model):
    name = models.CharField("Brand name", max_length=300)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RegexRule(models.Model):
    rule_text = models.CharField("Rule regex", max_length=200)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="regexes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rule_text
