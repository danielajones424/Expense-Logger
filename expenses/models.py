from datetime import date

class Expense:
    """How much was spent in a day."""

    def __init__(self, amount, category, description="", when=None):
        self.amount = float(amount)
        self.category = category.lower()
        self.description = description
        self.when = when if when is not None else date.today().isoformat()

    def is_in_month(self, month):
        return self.when.startswith(month)
    
    def __repr__(self):
        return (f"Expense(amount={self.amount!r}, category={self.category!r}, "
                f"description={self.description!r}, when={self.when!r})")

    def __str__(self):
        return f"{self.when}  {self.category:<12} ${self.amount:>8.2f}  {self.description}"

    def __eq__(self, other):
        if not isinstance(other, Expense):
            return NotImplemented
        return (self.amount, self.category, self.description, self.when) == \
               (other.amount, other.category, other.description, other.when)

    def __lt__(self, other):
        return self.when < other.when

    def to_dict(self):
        return {"amount": self.amount, "category": self.category,
                "description": self.description, "when": self.when}

    @classmethod
    def from_dict(cls, data):
        return cls(data["amount"], data["category"],
                   data.get("description", ""), data.get("when"))